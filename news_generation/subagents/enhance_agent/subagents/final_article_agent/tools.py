from google.adk.tools.tool_context import ToolContext
from ......utils.logging import news_gen_logger

def generate_article_description(content: str, tool_context: ToolContext):
    """Generate and save a concise article description to the tool context state.
    
    Args:
        content: The full article content in markdown format
        tool_context: Tool context for accessing state
    
    Returns:
        String with status message
    """
    try:
        news_gen_logger.info("[Tool Call] generate_article_description triggered by " + tool_context.agent_name)
        news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} state at entry: {tool_context.state}")
        news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} actions at entry: {vars(tool_context.actions)}")
        
        # Always update/create the article_description, don't check if it exists
        news_gen_logger.info(f"Setting article_description in state for {tool_context.agent_name}")
        tool_context.state['article_description'] = content
        news_gen_logger.info("article_description updated in state with content.")
        news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} state after update: {tool_context.state}")
        news_gen_logger.info(f"[DEBUG] {tool_context.agent_name} actions after update: {vars(tool_context.actions)}")
        
        return {
            "status": "SUCCESS",
            "message": "Generated final article description successfully saved",
            "article_description": content  # Explicitly return it in the result as well
        }
    except Exception as e:
        news_gen_logger.error("Error in [Tool Call] generate_article_description triggered by " + tool_context.agent_name)
        news_gen_logger.error(f"Exception details: {str(e)}")
        return {
            "status": "FAILED",
            "message": "Failed to generate final article description cause of exception ->" + str(e)
        }