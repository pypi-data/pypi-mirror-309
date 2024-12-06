"""Prompts."""

from typing import Any, Dict

PROMPTS: Dict[str, Any] = {}

## NEW
PROMPTS["entity_relationship_extraction"] = """You are a helpful assistant that helps a human analyst perform information discovery in the following domain.

# DOMAIN
{domain}

# GOAL
Given a document and a list of types, first, identify all present entities of those types and, then, all relationships among the identified entities.
Your goal is to highlight information that is relevant to the domain and the questions that may be asked on it.

Examples of possible questions:
{example_queries}

# STEPS
1. Identify all entities of the given types. Make sure to extract all and only the entities that are of one of the given types, ignore the others. Use singular names and split compound concepts when necessary (for example, from the sentence "they are movie and theater directors", you should extract the entities "movie director" and "theater director").
2. Identify all relationships between the entities found in step 1. Clearly resolve pronouns to their specific names to maintain clarity.
3. Double check that each entity identified in step 1 appears in at least one relationship. If not, add the missing relationships.

# EXAMPLE DATA
Types: [location, organization, person, communication]
Document: Radio City: Radio City is India's first private FM radio station and was started on 3 July 2001. It plays Hindi, English and regional songs. Radio City recently forayed into New Media in May 2008 with the launch of a music portal - PlanetRadiocity.com that offers music related news, videos, songs, and other music-related features."

Output:
{{
	'entities': [
	{{'name': 'Radio City', 'type': 'organization', 'desc': "Radio City is India's first private FM radio station."}},
	{{'name': 'India', 'type': 'location', 'desc': "The country of India."}},
	{{'name': 'FM radio station', 'type': 'communication', 'desc': "A radio station that broadcasts using frequency modulation."}},
	{{'name': 'English', 'type': 'communication', 'desc': "The English language."}},
	{{'name': 'Hindi', 'type': 'communication', 'desc': "The Hindi language."}},
	{{'name': 'New Media', 'type': 'communication', 'desc': "New Media is a term for all forms of media that are digital and/or interactive."}},
	{{'name': 'PlanetRadiocity.com', 'type': 'organization', 'desc': "PlanetRadiocity.com is an online music portal."}},
	{{'name': 'music portal', 'type': 'communication', 'desc': "A website that offers music related information."}},
	{{'name': 'news', 'type': 'communication', 'desc': "The concept of news."}},
	{{'name': 'video', 'type': 'communication', 'desc': "The concept of a video."}},
	{{'name': 'song', 'type': 'communication', 'desc': "The concept of a song."}}
	],
	'relationships': [
	{{'source': 'Radio City', 'target': 'India', 'desc': 'Radio City is located in India.'}},
	{{'source': 'Radio City', 'target': 'FM radio station', 'desc': 'Radio City is a private FM radio station started on 3 July 2001.'}},
	{{'source': 'Radio City', 'target': 'English', 'desc': 'Radio City broadcasts English songs.'}},
	{{'source': 'Radio City', 'target': 'Hindi', 'desc': 'Radio City broadcasts songs in the Hindi language.'}},
	{{'source': 'Radio City', 'target': 'PlanetRadiocity.com', 'desc': 'Radio City launched PlanetRadiocity.com in May 2008.'}},
	{{'source': 'PlanetRadiocity.com', 'target': 'music portal', 'desc': 'PlanetRadiocity.com is a music portal that offers music related news, videos and more.'}}
	],
	'other_relationships': [
	{{'source': 'Radio City', 'target': 'New Media', 'desc': 'Radio City forayed into New Media in May 2008.'}},
	{{'source': 'PlanetRadiocity.com', 'target': 'news', 'desc': 'PlanetRadiocity.com offers music related news.'}},
	{{'source': 'PlanetRadiocity.com', 'target': 'video', 'desc': 'PlanetRadiocity.com offers music related videos.'}},
	{{'source': 'PlanetRadiocity.com', 'target': 'song', 'desc': 'PlanetRadiocity.com offers songs.'}}
	]
}}

# REAL DATA
Types: {entity_types}
Document: {input_text}

Output:
"""

PROMPTS["entity_relationship_continue_extraction"] = "MANY entities were missed in the last extraction.  Add them below using the same format:"

PROMPTS["entity_relationship_gleaning_done_extraction"] = "Retrospectively check if all entities have been correctly identified: answer done if so, or continue if there are still entities that need to be added."

PROMPTS["entity_extraction_query"] = """You are a helpful assistant that helps a human analyst identify all the named entities present in the input query that are important for answering the query.

# Example 1
Query: Do the magazines Arthur's Magazine or First for Women have the same publisher?
Ouput: {{"entities": ["Arthur's Magazine", "First for Women"], "n": 2}}

# Example 2
Query: Which film has the director who was born earlier, Avatar II: The Return or The Interstellar?
Ouput: {{"entities": ["Avatar II: The Return", "The Interstellar"], "n": 2}}

# INPUT
Query: {query}
Output:
"""


PROMPTS[
	"summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given the current description, summarize it in a shorter but comprehensive description. Make sure to include all important information.
If the provided description is contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.

Current description:
{description}

Updated description:
"""


PROMPTS[
	"edges_group_similar"
] = """You are a helpful assistant responsible for maintaining a list of facts describing the relations between two entities so that information is not redundant.
Given a list of ids and facts, identify any facts that should be grouped together as they contain similar or duplicated information and provide a new summarized description for the group.

# EXAMPLE
Facts (id, description):
0, Mark is the dad of Luke
1, Luke loves Mark
2, Mark is always ready to help Luke
3, Mark is the father of Luke
4, Mark loves Luke very much

Ouput:
{{
	grouped_facts: [
	{{
		'ids': [0, 3],
		'description': 'Mark is the father of Luke'
	}},
	{{
		'ids': [1, 4],
		'description': 'Mark and Luke love each other very much'
	}}
	]
}}

# INPUT:
Facts:
{edge_list}

Ouput:
"""

PROMPTS["generate_response_query"] = """You are a helpful assistant gathering relevant data from the given tables to provide an helpful answer the user's query.

# GOAL
Your goal is to provide a response to the user's query, summarizing the relevant information in the input data tables.
If the answer cannot be inferred from the input data tables, just say no relevant information was found. Do not make anything up or add unrelevant information. Be concise.

# INPUT DATA TABLES
{context}

# QUERY
{query}

# OUTPUT
Follow this steps:
1. Read and understand the query and the information that would be relevant to answer it.
2. Carefully analyze the data tables provided and identify all relevant information that may help answer the user's query.
3. Generate a response to the user's query based on the information you have gathered.

Answer:
"""

## OLD

PROMPTS["fail_response"] = "Sorry, I'm not able to provide an answer to that question."

PROMPTS["default_text_separator"] = [
	# Paragraph separators
	"\n\n",
	"\r\n\r\n",
	# Line breaks
	"\n",
	"\r\n",
	# Sentence ending punctuation
	"。",  # Chinese period
	"．",  # Full-width dot
	".",  # English period
	"！",  # Chinese exclamation mark
	"!",  # English exclamation mark
	"？",  # Chinese question mark
	"?",  # English question mark
	# Whitespace characters
	" ",  # Space
	"\t",  # Tab
	"\u3000",  # Full-width space
	# Special characters
	"\u200b",  # Zero-width space (used in some Asian languages)
]
