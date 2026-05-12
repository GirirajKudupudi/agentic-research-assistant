"""
Web Search Tool — searches the web using DuckDuckGo.
No API key needed.
"""

from ddgs import DDGS
import time


def search_web(query: str, max_results: int = 5) -> list[dict]:
    """
    Search DuckDuckGo and return top results.
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        time.sleep(1)

        formatted = []
        for r in results:
            formatted.append({
                "title": r.get("title", ""),
                "snippet": r.get("body", ""),
                "url": r.get("href", ""),
            })

        return formatted if formatted else []

    except Exception as e:
        print(f"  [Debug] Search error: {e}")
        return []