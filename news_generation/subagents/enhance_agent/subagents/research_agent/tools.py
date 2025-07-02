from google.adk.tools.tool_context import ToolContext
from datetime import datetime

def save_research_findings(content: str, tool_context: ToolContext):
    """Save research findings to the state.
    
    Args:
        content: The research findings content in markdown format
        tool_context: Context for accessing and updating session state
        
    Returns:
        String with status message
    """
    if not tool_context:
        return "No tool context provided"
    
    # Create research findings object
    research_findings = {
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Save to state
    tool_context.state["research_findings"] = research_findings
    
    return "Successfully saved research findings to state"

def view_refined_article(tool_context: ToolContext):
    """View the refined article to research.
    
    Args:
        tool_context: Context for accessing session state
        
    Returns:
        String with information about the refined article
    """
    if not tool_context:
        return "No tool context provided"
        
    # Get refined article from state
    refined_article = tool_context.state.get("refined_article", {})
    
    if not refined_article:
        return "No refined article found"
    
    title = refined_article.get("title", "Untitled")
    content = refined_article.get("content", "")
    created_at = refined_article.get("created_at", "Unknown date")
    
    return f"Article: {title}\nCreated: {created_at}\n\n{content}"
