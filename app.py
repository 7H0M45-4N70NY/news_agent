from fastapi import FastAPI, Request, Header
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uuid

from dotenv import load_dotenv
from main import create_agent_runner,get_user_query_api,call_agent_async
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from news_generation.agent import UserQuery, NewsArticle
import json

# Load environment variables from .env file
load_dotenv()

# Initialize services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

app = FastAPI()

# CORS Configuration
origins = [
    "*"  # Allow all origins for now, but you should restrict this in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """This function is kept for potential future startup logic,
    but session creation is now handled on-demand."""
    pass


@app.post("/generate_news", response_model=NewsArticle)
async def generate_news_article(
    input: UserQuery,
    x_user_id: str = Header("default-user"),
    x_session_id: Optional[str] = Header("session_001")
):
    """Generates a news article, managing sessions dynamically per request."""
    session_id = x_session_id or f"session_{uuid.uuid4()}"
    user_id = x_user_id

    # Ensure the session exists, creating it if it's new
    try:
        await session_service.get_session(app_name="NewsArticleAPI", user_id=user_id, session_id=session_id)
    except ValueError:
        print(f"Creating new session: {session_id} for user: {user_id}")
        await session_service.create_session(
            session_id=session_id, user_id=user_id, app_name="NewsArticleAPI"
        )

    runner = await create_agent_runner(
        session_service=session_service,
        artifact_service=artifact_service,
        user_id=user_id,
        session_id=session_id
    )
    if not runner:
        return NewsArticle(title="Error", content="Failed to initialize agent runner.")
    
    user_query_content = get_user_query_api(input)
    final_response = await call_agent_async(user_query_content, runner, user_id, session_id)
    return final_response
