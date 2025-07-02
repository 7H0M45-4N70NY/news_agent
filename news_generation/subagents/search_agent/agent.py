from google.adk import Agent
from google.adk.tools import google_search

# Import agent-specific modules
from .prompt import SEARCH_AGENT_PROMPT

# Create the search agent
news_hunter = Agent(
    name="news_hunter",
    model="gemini-2.5-flash-preview-05-20",
    description="Specialized in discovering breaking news in categories like tech,education,world etc and the category is provided as input to the first agent",
    instruction=SEARCH_AGENT_PROMPT,
    tools=[google_search]
)
