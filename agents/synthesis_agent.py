"""
Synthesis Agent — merges results from document + web agents
and generates a unified answer with citations.

Placeholder for Day 1. Full LLM synthesis comes on Day 5.
"""

from state import AgentState


def synthesis_agent_node(state: AgentState) -> dict:
    """
    Combine all retrieved information and generate a final answer.
    
    Day 1: Simple concatenation of results.
    Day 5: Uses Ollama/Llama 3 for proper synthesis.
    """
    query = state["query"]
    doc_results = state.get("doc_results", [])
    web_results = state.get("web_results", [])

    parts = []
    sources = []

    for doc in doc_results:
        parts.append(f"Document: {doc['content']}")
        sources.append({"type": "document", "source": doc["source"], "page": doc["page"]})

    for web in web_results:
        parts.append(f"Web: {web['title']} - {web['snippet']}")
        sources.append({"type": "web", "title": web["title"], "url": web["url"]})

    if not parts:
        final_answer = f"No information found for: '{query}'"
    else:
        final_answer = (
            f"Results for: '{query}'\n\n"
            + "\n\n".join(parts)
            + "\n\n(Placeholder - Full LLM synthesis coming on Day 5)"
        )

    log_msg = f"[Synthesis Agent] Combined {len(doc_results)} doc + {len(web_results)} web results"

    return {
        "final_answer": final_answer,
        "sources": sources,
        "agent_logs": [log_msg],
    }