from google.adk.tools import ToolContext
from ......utils.logging import news_gen_logger


def exit_loop(refined_article: str, tool_context: ToolContext) -> dict:
    """
    Signal the completion of article refinement and exit the enhancement loop.
    """
    news_gen_logger.info(f"[Tool Call] exit_loop triggered by {tool_context.agent_name}")
    news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} state at entry: {tool_context.state}")
    news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} actions at entry: {vars(tool_context.actions)}")
    
    tool_context.state["refined_article"] = refined_article  # Always update with the article passed to exit_loop
    tool_context.actions.escalate = True

    news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} state after update: {tool_context.state}")
    news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} actions after update: {vars(tool_context.actions)}")
    
    return {}