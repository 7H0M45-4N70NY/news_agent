from .subagents.research_agent import research_agent
from .subagents.article_editor_agent import article_editor_agent
from .subagents.final_article_agent.agent import final_article_agent

from google.adk.agents import SequentialAgent


enhance_agent = SequentialAgent(
    name="enhance_agent_final",
    description="Enhance article with additional context and research",
    sub_agents=[research_agent, article_editor_agent, final_article_agent]
)