# duckduckgo/src/agenthub_tools/duckduckgo/tools.py
import json

from duckduckgo_search import DDGS

from agenthub_tools.core.base import tool

@tool("Search DuckDuckGo for a query and return results as a JSON string")
def search(
    query: str,
    max_results: int = 5,
    timeout: int = 10
) -> str:
    """
    Search DuckDuckGo for a query.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        timeout: Request timeout in seconds
        
    Returns:
        JSON string containing search results
    """
    with DDGS(timeout=timeout) as ddgs:
        results = ddgs.text(
            keywords=query,
            max_results=max_results
        )
        return json.dumps(list(results), indent=2)

@tool("Search DuckDuckGo News for recent articles matching the query")
def news(
    query: str,
    max_results: int = 5,
    timeout: int = 10
) -> str:
    """
    Search DuckDuckGo News for recent articles.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        timeout: Request timeout in seconds
        
    Returns:
        JSON string containing news results
    """
    with DDGS(timeout=timeout) as ddgs:
        results = ddgs.news(
            keywords=query,
            max_results=max_results
        )
        return json.dumps(list(results), indent=2)