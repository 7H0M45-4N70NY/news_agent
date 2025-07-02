from google.adk.tools.tool_context import ToolContext
from datetime import datetime

def save_research_to_state(research_results: str, tool_context: ToolContext) -> dict:
    """Save research results to session state, updating existing articles or adding new ones.
    
    Args:
        research_results: JSON string containing array of article objects to save
        tool_context: Context for accessing and updating session state
        
    Returns:
        A confirmation message with details about saved articles
    """
    import json
    
    try:
        # Parse the JSON string into a Python object
        articles_to_save = json.loads(research_results)
        if not isinstance(articles_to_save, list):
            articles_to_save = [articles_to_save]
    except json.JSONDecodeError:
        return {
            "action": "save_research",
            "status": "error",
            "message": "Invalid JSON format for research_results"
        }
    
    # Get the current articles, defaulting to an empty list
    articles = tool_context.state.get("researched_articles", [])
    
    # Process each article
    new_articles = 0
    updated_articles = 0
    article_titles = []
    
    for article in articles_to_save:
        if not isinstance(article, dict):
            continue
            
        # Add timestamp
        article["saved_at"] = datetime.now().isoformat()
        
        # Store article title for reporting
        if "title" in article:
            article_titles.append(article["title"])
        
        # Check if article already exists (by URL or title)
        existing_article = False
        for i, existing in enumerate(articles):
            if (("url" in article and "url" in existing and article["url"] == existing["url"]) or 
                ("title" in article and "title" in existing and article["title"] == existing["title"])):
                articles[i] = article  # Replace with updated version
                existing_article = True
                updated_articles += 1
                break
                
        # If article doesn't exist, add it
        if not existing_article:
            articles.append(article)
            new_articles += 1
    
    # Update state with the modified list
    tool_context.state["researched_articles"] = articles
    
    # Return confirmation
    return {
        "action": "save_research",
        "new_articles": new_articles,
        "updated_articles": updated_articles,
        "total_articles": len(articles),
        "titles": article_titles[:3],  # Show first 3 titles
        "message": f"Saved {new_articles} new and updated {updated_articles} existing articles. Total: {len(articles)}"
    }
