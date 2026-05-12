"""
Synthesis Agent — merges results from document + web agents
and generates a unified answer using Ollama/Llama 3.2.
"""

from state import AgentState
from langchain_ollama import ChatOllama


def synthesis_agent_node(state: AgentState) -> dict:
    """
    Combine all retrieved information and use Llama 3.2
    to generate a coherent answer with citations.
    """
    query = state["query"]
    doc_results = state.get("doc_results", [])
    web_results = state.get("web_results", [])

    # Build context from all sources
    context_parts = []
    sources = []

    for i, doc in enumerate(doc_results):
        context_parts.append(
            f"[Document Source {i+1} - {doc['source']}, Page {doc['page']}]\n{doc['content']}"
        )
        sources.append({"type": "document", "source": doc["source"], "page": doc["page"]})

    for i, web in enumerate(web_results):
        context_parts.append(
            f"[Web Source {i+1} - {web['title']}]\n{web['snippet']}\nURL: {web['url']}"
        )
        sources.append({"type": "web", "title": web["title"], "url": web["url"]})

    if not context_parts:
        return {
            "final_answer": f"I couldn't find any information about: '{query}'",
            "sources": [],
            "agent_logs": ["[Synthesis Agent] No context available to synthesize"],
        }

    context = "\n\n".join(context_parts)

    # Build the prompt
    prompt = f"""You are a research assistant. Answer the user's question based ONLY on the provided sources below. 

Rules:
- Use only information from the sources
- Mention which source you're using (e.g. "According to Document Source 1..." or "Based on Web Source 2...")
- If sources don't fully answer the question, say what you found and what's missing
- Be concise and clear

SOURCES:
{context}

QUESTION: {query}

ANSWER:"""

    # Call Ollama
    llm = ChatOllama(model="llama3.2:1b", temperature=0.3)
    response = llm.invoke(prompt)
    final_answer = response.content

    log_msg = f"[Synthesis Agent] Generated answer from {len(doc_results)} doc + {len(web_results)} web sources"

    return {
        "final_answer": final_answer,
        "sources": sources,
        "agent_logs": [log_msg],
    }