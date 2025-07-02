from google.adk import Agent

from .prompt import FINAL_ARTICLE_GENERATION_PROMPT
from pydantic import BaseModel, Field

class NewsArticle(BaseModel):
    title: str = Field(description="The title of the generated news article.")
    content: str = Field(description="The full content of the generated news article.")

# Create the final article agent
final_article_agent = Agent(
    name="tech_final_article_generator",
    model="gemini-2.0-flash",
    description="Expert final article generator that creates concise, informative, and impactful news articles",
    instruction=FINAL_ARTICLE_GENERATION_PROMPT,
    output_schema=NewsArticle
)
