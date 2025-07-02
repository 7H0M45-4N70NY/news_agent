from google.adk import Agent
from google.adk.tools import google_search

from google.adk.tools.agent_tool import AgentTool

# Import agent-specific modules
from .tools import save_research_findings, view_refined_article
from .prompt import RESEARCH_AGENT_PROMPT, RESEARCH_AGENT_PROMPT_MAIN

# Create the agent tools for research agent
research_agent_google_search_tool = Agent(
    name="tech_research_specialist_google_search_tool",
    model="gemini-2.0-flash",
    description="Expert technology researcher that gathers in-depth information on tech topics",
    instruction=RESEARCH_AGENT_PROMPT,
    tools=[google_search]
)

# Create the research agent
research_agent = Agent(
    name="tech_research_specialist",
    model="gemini-2.0-flash",
    description="Expert technology researcher that gathers in-depth information on tech topics",
    instruction=RESEARCH_AGENT_PROMPT_MAIN,
    tools=[AgentTool(research_agent_google_search_tool)]
)



