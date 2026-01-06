from google.adk.agents import Agent, SequentialAgent
from google.adk.model.google_llm import Gemini
from google.genai import types
from google.adk.tools import google_search

retry_config = types.HttpRetyOptions(
    attempts = 5,
    exp_base= 7,
    initial_delay = 1,
    http_status_codes = [429, 500, 503, 504 ],
)


"""
Blog Post Creation with Sequential Agents
Let's build a system with three specialized agents:

Outline Agent - Creates a blog outline for a given topic
Writer Agent - Writes a blog post
Editor Agent - Edits a blog post draft for clarity and structure

"""

outline_agent = Agent(
    name ="Outline Agent",
    model =Gemini(
        model="gemini-2.5-flash-lite",
        retry_config=retry_config
    ),
    instuction = """Create a blog outline for the given topic with:
    1. A catchy headline
    2. An introduction hook
    3. 3-5 main sections with 2-3 bullet points for each
    4. A concluding thought""",
    output_key ="blog_outline"
)
writer_agent = Agent(
    name = "Writer Agent",
    model = Gemini(
        model="gemini-2.5-flash-lite",
        retry_config=retry_config,
    ),
    instruction = """Following this outline strictly: {blog_outline}
    Write a brief, 200 to 300-word blog post with an engaging and informative tone.""",
    output_key = "blog_draft"
)
editor_agent = Agent(
    name ="Editor Agent",
    model = Gemini(
        model="gemini-2.5-flash-lite",
        retry_config= retry_config,
    ),
    instruction ="""Edit this draft: {blog_draft}
    Your task is to polish the text by fixing any grammatical errors, improving the flow and sentence structure, and enhancing overall clarity.""",
    output_key ="final_blog_post"
)

blog_post_agent = SequentialAgent(
    name ="Blog Pipeline",
    sub_agents =[outline_agent, writer_agent, editor_agent]
)
