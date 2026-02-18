import asyncio
import threading
import time
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from news_generation.agent import root_agent
from custom_logger import logger
from news_generation.agent import UserQuery
from news_generation.subagents.enhance_agent.subagents.final_article_agent.agent import MultiNewsArticle
from token_tracker import token_tracker
import json

# Load environment variables from .env file
load_dotenv()

SESSION_ID = "session_001"

# Session management
session_registry = {}  # Track sessions for cleanup

def cleanup_old_sessions(session_service: InMemorySessionService, max_age_hours: int = 1):
    """Background thread to clean up expired sessions"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        try:
            current_time = time.time()
            expired_sessions = [
                session_id for session_id, info in session_registry.items()
                if (current_time - info["created_at"]) / 3600 >= max_age_hours
            ]
            
            for session_id in expired_sessions:
                session_info = session_registry[session_id]
                try:
                    loop.run_until_complete(
                        session_service.delete_session(
                            app_name=session_info["app_name"],
                            user_id=session_info["user_id"],
                            session_id=session_id
                        )
                    )
                    del session_registry[session_id]
                    print(f"Cleaned up expired session: {session_id}")
                except Exception as e:
                    print(f"Error cleaning up session {session_id}: {e}")
            
            time.sleep(300)  # Check every 5 minutes
            
        except Exception as e:
            print(f"Session cleanup error: {e}")
            time.sleep(300)

def start_session_cleanup(session_service: InMemorySessionService, max_age_hours: int = 1):
    """Start background session cleanup thread"""
    cleanup_thread = threading.Thread(
        target=cleanup_old_sessions,
        args=(session_service, max_age_hours),
        daemon=True
    )
    cleanup_thread.start()
    return cleanup_thread

async def create_agent_runner(
    session_service: InMemorySessionService,
    artifact_service: InMemoryArtifactService,
    user_id="thomas",
    app_name="Thomas AI",
    session_id=SESSION_ID,
    session_ttl_hours=1
):
    """Create agent runner with session tracking"""
    try:
        initial_state = {
            "article_title": "",
            "article_content": "",
            "article_description": "",
            "article_image": "",
            "downloaded_images": {},
            "image_to_analyze": "",
            "image_analysis_result": ""
        }
        
        # Create session
        stateful_session = await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )
        
        # Register session for cleanup
        session_registry[session_id] = {
            "created_at": time.time(),
            "app_name": app_name,
            "user_id": user_id
        }
        
        # Create runner
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            app_name=app_name,
            artifact_service=artifact_service,
        )

        return runner

    except Exception as e:
        print(f"Error creating agent runner: {e}")
        return None


def get_user_query_api(user_input: UserQuery):
    """Create user query content from input"""
    user_query_content = types.Content(
        role="user", parts=[types.Part(text=user_input.model_dump_json())]
    )
    return user_query_content


def get_user_query():
    """Get default user query for testing"""
    user_input = UserQuery(topic="Sports", country="India")
    user_query_content = types.Content(
        role="user", parts=[types.Part(text=user_input.model_dump_json())]
    )
    return user_query_content

async def call_agent_async(
    user_query_content: types.Content,
    runner: Runner,
    user_id="thomas",
    session_id=SESSION_ID
):
    """Execute agent and return structured response"""
    try:
        final_response_text = ""
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_query_content):
            # Track token usage from event metadata
            if hasattr(event, 'usage_metadata') and event.usage_metadata:
                input_tokens = getattr(event.usage_metadata, 'prompt_token_count', 0) or 0
                output_tokens = getattr(event.usage_metadata, 'candidates_token_count', 0) or 0
                if input_tokens > 0 or output_tokens > 0:
                    token_tracker.track(input_tokens, output_tokens)
            
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_part = event.content.parts[0].text
                    if response_part:
                        final_response_text = response_part

        if final_response_text:
            try:
                # Try to parse as JSON
                if isinstance(final_response_text, str):
                    # Strip markdown code blocks if present
                    cleaned_text = final_response_text.strip()
                    if cleaned_text.startswith("```json"):
                        cleaned_text = cleaned_text[7:]  # Remove ```json
                    elif cleaned_text.startswith("```"):
                        cleaned_text = cleaned_text[3:]  # Remove ```
                    if cleaned_text.endswith("```"):
                        cleaned_text = cleaned_text[:-3]  # Remove trailing ```
                    cleaned_text = cleaned_text.strip()
                    
                    final_response_data = json.loads(cleaned_text)
                else:
                    final_response_data = final_response_text
                
                # Validate against MultiNewsArticle schema
                multi_news_article = MultiNewsArticle.model_validate(final_response_data)
                return multi_news_article.model_dump()
            except json.JSONDecodeError:
                # If not valid JSON, return error with the text received
                logger.warning(f"Response is not valid JSON: {final_response_text[:100]}")
                return {"articles": [{"title": "Error", "content": f"Agent returned non-JSON response: {final_response_text[:200]}", "word_count": 0}]}
            except Exception as e:
                logger.error(f"Failed to parse response: {e}")
                return {"articles": [{"title": "Error", "content": f"Failed to parse response: {str(e)}", "word_count": 0}]}
        else:
            return {"articles": [{"title": "Error", "content": "No valid final response was generated.", "word_count": 0}]}

    except Exception as e:
        logger.error(f"Error in call_agent_async: {str(e)}")
        raise


async def main():
    """Main execution function"""
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    # Start session cleanup
    start_session_cleanup(session_service, max_age_hours=1) 

    # Create session
    await session_service.create_session(session_id=SESSION_ID)

    # Run agent
    user_query_content = get_user_query()
    runner = await create_agent_runner(
        session_service=session_service,
        artifact_service=artifact_service,
        user_id="local_user",
        session_id=SESSION_ID,
        session_ttl_hours=1
    )
    
    if runner:
        final_response = await call_agent_async(
            user_query_content,
            runner,
            user_id="local_user",
            session_id=SESSION_ID
        )
        print(f"\nFinal structured response:\n{json.dumps(final_response, indent=2)}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExecution interrupted by user.")
