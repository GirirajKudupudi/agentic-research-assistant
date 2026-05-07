"""
Document Agent — retrieves relevant chunks from uploaded PDFs.

Placeholder for Day 1. Full RAG pipeline comes on Day 2.
"""

from state import AgentState


def document_agent_node(state: AgentState) -> dict:
    """
    Search uploaded documents for relevant information.
    
    Day 1: Returns placeholder.
    Day 2: Connects to ChromaDB with real PDF retrieval.
    """
    query = state["query"]

    doc_results = [
        {
            "content": f"[Placeholder] No documents indexed yet for: '{query}'",
            "source": "No documents loaded",
            "page": 0,
        }
    ]

    log_msg = "[Document Agent] Searched documents (placeholder — no PDFs indexed)"

    return {
        "doc_results": doc_results,
        "agent_logs": [log_msg],
    }