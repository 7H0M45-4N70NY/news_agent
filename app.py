from fastapi import FastAPI, Request, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import uuid
import logging
import os

from dotenv import load_dotenv
from main import create_agent_runner,get_user_query_api,call_agent_async,start_session_cleanup
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from news_generation.agent import UserQuery, MultiNewsArticle
from token_tracker import token_tracker
import json

# Disable uvicorn logs
logging.getLogger("uvicorn").setLevel(logging.WARNING)
logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
logging.getLogger("uvicorn.asgi").setLevel(logging.WARNING)

# Disable verbose ADK/Gemini logs
logging.getLogger("google.adk").setLevel(logging.WARNING)
logging.getLogger("google.genai").setLevel(logging.WARNING)
logging.getLogger("google.genai.client").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("google.cloud").setLevel(logging.ERROR)
logging.getLogger("google.cloud.aiplatform").setLevel(logging.ERROR)

# Configure root logger
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


# Load environment variables from .env file
load_dotenv()

# Initialize services
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()

app = FastAPI(title="AI News Generator", description="Generate trending news articles using AI")

# Mount static files (assets folder)
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

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
    """Initialize session cleanup on startup"""
    # Start session cleanup background thread
    start_session_cleanup(session_service, max_age_hours=1)


@app.get("/")
async def serve_index():
    """Serve the landing page"""
    return FileResponse("index.html", media_type="text/html")


@app.post("/generate_news", response_model=MultiNewsArticle)
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
        return {"articles": [{"title": "Error", "content": "Failed to initialize agent runner.", "word_count": 0}]}
    
    user_query_content = get_user_query_api(input)
    final_response = await call_agent_async(user_query_content, runner, user_id, session_id)
    
    # Print token usage summary
    token_tracker.print_summary()
    
    return final_response


@app.get("/token-stats")
async def get_token_stats():
    """Get token usage statistics"""
    return token_tracker.get_summary()


