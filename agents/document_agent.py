"""
Document Agent — retrieves relevant chunks from uploaded PDFs
using ChromaDB vector search.
"""

from state import AgentState
from tools.rag_tool import search_documents


def document_agent_node(state: AgentState) -> dict:
    """
    Search uploaded documents for relevant information.
    Uses ChromaDB similarity search to find the best matching chunks.
    """
    query = state["query"]

    results = search_documents(query, top_k=4)

    if not results:
        log_msg = "[Document Agent] No documents indexed — upload a PDF first"
        doc_results = []
    else:
        log_msg = f"[Document Agent] Found {len(results)} relevant chunks"
        doc_results = [
            {
                "content": r["content"],
                "source": r["source"],
                "page": r["page"],
            }
            for r in results
        ]

    return {
        "doc_results": doc_results,
        "agent_logs": [log_msg],
    }