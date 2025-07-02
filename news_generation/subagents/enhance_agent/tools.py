from google.adk.tools.tool_context import ToolContext
from datetime import datetime
import re

def view_research_findings(tool_context: ToolContext):
    """View the research findings from the research agent.
    
    Args:
        tool_context: Context for accessing session state
        
    Returns:
        String with information about the research findings
    """
    if not tool_context:
        return "No tool context provided"
        
    # Get research findings from state
    findings = tool_context.state.get("research_findings", {})
    
    if not findings:
        return "No research findings found"
    
    content = findings.get("content", "")
    created_at = findings.get("created_at", "Unknown date")
    
    return f"Research Findings\nCreated: {created_at}\n\n{content}"

def view_latest_article(tool_context: ToolContext):
    """View the most recently refined article.
    
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

def save_enhanced_article(content: str, tool_context: ToolContext):
    """Save the enhanced article content with additional research.
    
    Args:
        content: The enhanced article content in markdown format
        tool_context: Context for accessing and updating session state
        
    Returns:
        String with status message
    """
    if not tool_context:
        return "No tool context provided"
    
    # Extract title from the first markdown heading
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    title = title_match.group(1) if title_match else "Enhanced Article"
    
    # Create article object
    enhanced_article = {
        "title": title,
        "content": content,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "enhanced"
    }
    
    # Save to state
    tool_context.state["enhanced_article"] = enhanced_article
    
    # Add to history
    history = tool_context.state.get("enhanced_articles_history", [])
    history.append(enhanced_article)
    tool_context.state["enhanced_articles_history"] = history
    
    return f"Successfully saved enhanced article: {title}"

def view_enhanced_article(tool_context: ToolContext):
    """View the currently enhanced article.
    
    Args:
        tool_context: Context for accessing session state
        
    Returns:
        String with information about the enhanced article
    """
    if not tool_context:
        return "No tool context provided"
        
    # Get enhanced article from state
    enhanced_article = tool_context.state.get("enhanced_article", {})
    
    if not enhanced_article:
        return "No enhanced article found"
    
    title = enhanced_article.get("title", "Untitled")
    content = enhanced_article.get("content", "")
    created_at = enhanced_article.get("created_at", "Unknown date")
    
    return f"Enhanced Article: {title}\nCreated: {created_at}\n\n{content}"

def compare_articles(tool_context: ToolContext):
    """Compare the original refined article with the enhanced version.
    
    Args:
        tool_context: Context for accessing session state
        
    Returns:
        String with comparison information
    """
    if not tool_context:
        return "No tool context provided"
        
    # Get both articles from state
    refined_article = tool_context.state.get("refined_article", {})
    enhanced_article = tool_context.state.get("enhanced_article", {})
    
    if not refined_article:
        return "No refined article found for comparison"
    
    if not enhanced_article:
        return "No enhanced article found for comparison"
    
    refined_title = refined_article.get("title", "Untitled")
    enhanced_title = enhanced_article.get("title", "Untitled")
    
    refined_created = refined_article.get("created_at", "Unknown date")
    enhanced_created = enhanced_article.get("created_at", "Unknown date")
    
    # Calculate word counts
    refined_content = refined_article.get("content", "")
    enhanced_content = enhanced_article.get("content", "")
    
    refined_word_count = len(refined_content.split())
    enhanced_word_count = len(enhanced_content.split())
    word_diff = enhanced_word_count - refined_word_count
    
    return f"""
# Article Comparison

## Original Article
- Title: {refined_title}
- Created: {refined_created}
- Word Count: {refined_word_count}

## Enhanced Article
- Title: {enhanced_title}
- Created: {enhanced_created}
- Word Count: {enhanced_word_count}

## Difference
- Added Words: {word_diff if word_diff > 0 else 0}
- Removed Words: {abs(word_diff) if word_diff < 0 else 0}
- Net Change: {word_diff:+d} words ({(word_diff/refined_word_count*100 if refined_word_count > 0 else 0):.1f}%)
"""
