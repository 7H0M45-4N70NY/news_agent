from google.adk import Agent

from .prompt import FINAL_ARTICLE_GENERATION_PROMPT
from pydantic import BaseModel, Field

class ArticleContent(BaseModel):
    title: str = Field(description="The title of the generated news article.")
    content: str = Field(description="The content of the news article. Length varies naturally based on story importance and depth needed.")
    word_count: int = Field(description="Approximate word count of the article content.")

class MultiNewsArticle(BaseModel):
    articles: list[ArticleContent] = Field(description="List of 1-3 generated news articles, ordered by priority/importance.")

# Create the final article agent
final_article_agent = Agent(
    name="tech_final_article_generator",
    model="gemini-2.5-flash-lite",
    description="Expert final article generator that creates multiple concise, informative, and impactful news articles with dynamic length allocation",
    instruction=FINAL_ARTICLE_GENERATION_PROMPT
)
