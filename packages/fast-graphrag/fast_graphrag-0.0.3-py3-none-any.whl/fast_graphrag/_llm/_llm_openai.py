"""LLM Services module."""

import asyncio
from dataclasses import dataclass, field
from itertools import chain
from typing import Any, List, Optional, Tuple, Type, cast

import instructor
import numpy as np
from openai import APIConnectionError, AsyncOpenAI, RateLimitError
from pydantic import BaseModel
from tenacity import (
    AsyncRetrying,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from fast_graphrag._exceptions import LLMServiceNoResponseError
from fast_graphrag._types import BTResponseModel, GTResponseModel
from fast_graphrag._utils import TOKEN_TO_CHAR_RATIO, logger, throttle_async_func_call

from ._base import BaseEmbeddingService, BaseLLMService

TIMEOUT_SECONDS = 180.0


@dataclass
class OpenAILLMService(BaseLLMService):
    """LLM Service for OpenAI LLMs."""

    model: Optional[str] = field(default="gpt-4o-mini")

    def __post_init__(self):
        logger.debug("Initialized OpenAILLMService with patched OpenAI client.")
        self.llm_async_client: instructor.AsyncInstructor = instructor.from_openai(
            AsyncOpenAI(base_url=self.base_url, api_key=self.api_key, timeout=TIMEOUT_SECONDS)
        )

    @throttle_async_func_call(max_concurrent=256, stagger_time=0.001, waitting_time=0.001)
    async def send_message(
        self,
        prompt: str,
        model: str | None = None,
        system_prompt: str | None = None,
        history_messages: list[dict[str, str]] | None = None,
        response_model: Type[GTResponseModel] | None = None,
        **kwargs: Any,
    ) -> Tuple[GTResponseModel, list[dict[str, str]]]:
        """Send a message to the language model and receive a response.

        Args:
            prompt (str): The input message to send to the language model.
            model (str): The name of the model to use. Defaults to the model provided in the config.
            system_prompt (str, optional): The system prompt to set the context for the conversation. Defaults to None.
            history_messages (list, optional): A list of previous messages in the conversation. Defaults to empty.
            response_model (Type[T], optional): The Pydantic model to parse the response. Defaults to None.
            **kwargs: Additional keyword arguments that may be required by specific LLM implementations.

        Returns:
            str: The response from the language model.
        """
        logger.debug(f"Sending message with prompt: {prompt}")
        model = model or self.model
        if model is None:
            raise ValueError("Model name must be provided.")
        messages: list[dict[str, str]] = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
            logger.debug(f"Added system prompt: {system_prompt}")

        if history_messages:
            messages.extend(history_messages)
            logger.debug(f"Added history messages: {history_messages}")

        messages.append({"role": "user", "content": prompt})

        llm_response: GTResponseModel = await self.llm_async_client.chat.completions.create(
            model=model,
            messages=messages,  # type: ignore
            response_model=response_model.Model
            if response_model and issubclass(response_model, BTResponseModel)
            else response_model,
            **kwargs,
            max_retries=AsyncRetrying(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)),
        )

        if not llm_response:
            logger.error("No response received from the language model.")
            raise LLMServiceNoResponseError("No response received from the language model.")

        messages.append(
            {
                "role": "assistant",
                "content": llm_response.model_dump_json() if isinstance(llm_response, BaseModel) else str(llm_response),
            }
        )
        logger.debug(f"Received response: {llm_response}")

        if response_model and issubclass(response_model, BTResponseModel):
            llm_response = cast(GTResponseModel, cast(BTResponseModel.Model, llm_response).to_dataclass(llm_response))

        return llm_response, messages


@dataclass
class OpenAIEmbeddingService(BaseEmbeddingService):
    """Base class for Language Model implementations."""

    embedding_dim: int = field(default=1536)
    max_request_tokens: int = 8000
    model: Optional[str] = field(default="text-embedding-3-small")

    def __post_init__(self):
        self.embedding_async_client: AsyncOpenAI = AsyncOpenAI(
            base_url=self.base_url, api_key=self.api_key, timeout=TIMEOUT_SECONDS
        )
        logger.debug("Initialized OpenAIEmbeddingService with OpenAI client.")

    async def get_embedding(
        self, texts: list[str], model: Optional[str] = None
    ) -> np.ndarray[Any, np.dtype[np.float32]]:
        """Get the embedding representation of the input text.

        Args:
            texts (str): The input text to embed.
            model (str, optional): The name of the model to use. Defaults to the model provided in the config.

        Returns:
            list[float]: The embedding vector as a list of floats.
        """
        logger.debug(f"Getting embedding for texts: {texts}")
        model = model or self.model
        if model is None:
            raise ValueError("Model name must be provided.")

        # Chunk the requests to size limits
        max_chunk_length = self.max_request_tokens * TOKEN_TO_CHAR_RATIO
        text_chunks: List[List[str]] = []

        current_chunk: List[str] = []
        current_chunk_length = 0
        for text in texts:
            text_length = len(text)
            if text_length + current_chunk_length > max_chunk_length:
                text_chunks.append(current_chunk)
                current_chunk = []
                current_chunk_length = 0
            current_chunk.append(text)
            current_chunk_length += text_length
        text_chunks.append(current_chunk)

        response = await asyncio.gather(*[self._embedding_request(chunk, model) for chunk in text_chunks])

        data = chain(*[r.data for r in response])
        embeddings = np.array([dp.embedding for dp in data])
        logger.debug(f"Received embedding response: {len(embeddings)} embeddings")

        return embeddings

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type((RateLimitError, APIConnectionError, TimeoutError)),
    )
    async def _embedding_request(self, input: List[str], model: str) -> Any:
        return await self.embedding_async_client.embeddings.create(model=model, input=input, encoding_format="float")
