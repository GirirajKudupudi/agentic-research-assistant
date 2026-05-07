"""
Web Search Agent — searches the web via DuckDuckGo.

Placeholder for Day 1. Full search integration comes on Day 3.
"""

from state import AgentState


def web_agent_node(state: AgentState) -> dict:
    """
    Search the web for relevant information.
    
    Day 1: Returns placeholder.
    Day 3: Connects to DuckDuckGo search.
    """
    query = state["query"]

    web_results = [
        {
            "title": f"[Placeholder] Web search for: '{query}'",
            "snippet": "Web search will be connected on Day 3.",
            "url": "https://example.com",
        }
    ]

    log_msg = "[Web Agent] Searched web (placeholder — not connected yet)"

    return {
        "web_results": web_results,
        "agent_logs": [log_msg],
    }
