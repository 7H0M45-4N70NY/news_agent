import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from google.genai import types
from news_generation.agent import root_agent
from custom_logger import logger
from news_generation.agent import UserQuery
from news_generation.subagents.enhance_agent.subagents.final_article_agent.agent import NewsArticle
import json

# Load environment variables from .env file
load_dotenv()

# Initialize services
# These will now be created and managed in the entry point (main or api)

SESSION_ID = "session_001"

async def create_agent_runner(
    session_service: InMemorySessionService,
    artifact_service: InMemoryArtifactService,
    user_id="thomas",
    app_name="Thomas AI",
    session_id=SESSION_ID
    ):
    try:
        # Create a NEW session
        APP_NAME = app_name
        SESSION_ID=session_id
        USER_ID=user_id
        initial_state = {
            "article_title": "",
            "article_content": "",
            "article_description": "",
            "article_image": "",
            "downloaded_images": {},
            "image_to_analyze": "",
            "image_analysis_result": ""
        }
        stateful_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_state
        )
        
        runner = Runner(
            agent=root_agent,
            session_service=session_service,
            app_name=APP_NAME,
            artifact_service=artifact_service,
        )

        return runner

    except Exception as e:
        print(f"Error creating agent runner: {e}")
        return None


def get_user_query_api(user_input:UserQuery):
    user_query_content = types.Content(
        role="user", parts=[types.Part(text=user_input.model_dump_json())]
    )
    return user_query_content


def get_user_query():
    user_input = UserQuery(topic="Sports",country="India")
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
    try:
        print(f"\n>>> User Query Content: {user_query_content}")

        final_response_text = ""
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=user_query_content):
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_part = event.content.parts[0].text
                    try:
                        # The most reliable way to find the final response is to see if it
                        # successfully parses into our target Pydantic model.
                        news_article = NewsArticle.model_validate_json(response_part)
                        
                        # If parsing succeeds, we have our final article.
                        print(f"\n<<< Agent Response (Title): {news_article.title}")
                        print(f"<<< Agent Response (Content): {news_article.content}")
                        final_response_text = news_article.model_dump_json(indent=2)
                        
                    except Exception as json_e:
                        # If parsing fails, it's likely an intermediate response.
                        # We can log it for debugging but will otherwise ignore it and
                        # wait for the actual final response that matches our schema.
                        print(f"Ignoring intermediate response that failed to parse: {json_e}")
                        pass # Continue to the next event

        # After the loop, process the final response.
        if final_response_text:
            # The response is already a validated JSON string from the model dump.
            final_response_data = json.loads(final_response_text)
            return final_response_data
        else:
            return {"error": "No valid final response matching the NewsArticle schema was generated."}

    except Exception as e:
        logger.error(f"Error in call_agent_async: {str(e)}")
        raise


async def main():
    # When running main.py directly, create local services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()

    # Create the session before using it
    await session_service.create_session(session_id=SESSION_ID)

    user_query_content = get_user_query()
    runner = await create_agent_runner(
        session_service=session_service,
        artifact_service=artifact_service,
        user_id="local_user",
        session_id=SESSION_ID
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
