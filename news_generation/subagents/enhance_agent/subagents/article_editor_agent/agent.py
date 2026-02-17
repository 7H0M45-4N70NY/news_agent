from google.adk import Agent
from .prompt import  ARTICLE_EDITOR_PROMPT_V2

# Create the article editor agent
article_editor_agent = Agent(
    name="tech_article_editor",
    model="gemini-2.5-flash-lite",
    description="Expert editor that makes minimal, high-impact edits to enhance article clarity and context",
    instruction=ARTICLE_EDITOR_PROMPT_V2,
    output_key="refined_article"
)
