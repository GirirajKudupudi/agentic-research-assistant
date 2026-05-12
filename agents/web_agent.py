"""
Web Search Agent — searches the web via DuckDuckGo.
"""

from state import AgentState
from tools.search_tool import search_web


def web_agent_node(state: AgentState) -> dict:
    """
    Search the web for relevant information using DuckDuckGo.
    """
    query = state["query"]

    results = search_web(query, max_results=5)

    if not results:
        log_msg = f"[Web Agent] No web results found for: '{query}'"
        web_results = []
    else:
        log_msg = f"[Web Agent] Found {len(results)} web results"
        web_results = results

    return {
        "web_results": web_results,
        "agent_logs": [log_msg],
    }