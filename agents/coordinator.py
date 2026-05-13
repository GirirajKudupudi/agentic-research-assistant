"""
Coordinator Agent — the brain of the research assistant.

Uses Llama 3.2 to analyze the query and decide which agents to call.
"""

from state import AgentState
from langchain_ollama import ChatOllama


def coordinator_node(state: AgentState) -> dict:
    """
    Use the LLM to analyze the query and decide the plan.
    """
    query = state["query"]

    prompt = f"""You are a query router. Based on the user's question, decide which agents to call.

Available agents:
- document: Search uploaded PDF documents for information
- web: Search the internet for current information

Rules:
- If the user mentions "document", "pdf", "uploaded", "file" → include "document"
- If the user asks about current events, general knowledge, or how-to → include "web"
- If unclear, include both "document" and "web"
- Respond with ONLY the agent names separated by commas, nothing else

Examples:
"What does the PDF say about sales?" → document
"What is machine learning?" → web
"Compare what the document says with latest research" → document,web
"Tell me about neural networks" → web
"Summarize the uploaded report" → document

User question: {query}

Agents to call:"""

    llm = ChatOllama(model="llama3.2:1b", temperature=0)
    response = llm.invoke(prompt)
    answer = response.content.strip().lower()

    # Parse the LLM response
    plan = []
    if "document" in answer:
        plan.append("document")
    if "web" in answer:
        plan.append("web")

    # Fallback if LLM gave unexpected output
    if not plan:
        plan = ["document", "web"]

    plan.append("synthesis")

    log_msg = f"[Coordinator] Query: '{query}' → LLM decided: {plan}"

    return {
        "agent_plan": plan,
        "agent_logs": [log_msg],
    }