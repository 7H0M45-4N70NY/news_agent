from google.adk import Agent

from .subagents.search_agent import news_hunter
from .subagents.enhance_agent.agent import enhance_agent
from google.adk.tools.agent_tool import AgentTool
from pydantic import BaseModel, Field
from .prompt import (NEW_ARTICLE_GENERATION_PROMPT)



class UserQuery(BaseModel):
    topic: str = Field(description="The topic of the news article to generate.")
    country: str = Field(description="The country for which the news article is relevant.")

class NewsArticle(BaseModel):
    title: str = Field(description="The title of the generated news article.")
    content: str = Field(description="The full content of the generated news article.")


# Main coordinator agent
root_agent = Agent(
    name="new_article_creation_agent",
    model="gemini-2.0-flash",
    description="Coordinates the workflow for generating technology news articles",
    instruction=NEW_ARTICLE_GENERATION_PROMPT,
    input_schema=UserQuery,
    tools=[
        # Agent tools
        AgentTool(news_hunter)
    ],
    sub_agents=[enhance_agent]
)       
