"""
Coordinator Agent — the brain of the research assistant.

Receives the user query and decides which specialist agents to call.
"""

from state import AgentState


def coordinator_node(state: AgentState) -> dict:
    """
    Analyze the query and decide which agents to call.
    
    Simple keyword routing for now.
    Day 4: we'll upgrade this to use LLM-based planning.
    """
    query = state["query"].lower()
    plan = []

    doc_keywords = ["document", "pdf", "uploaded", "file", "paper",
                    "report", "according to", "in the", "from the"]
    web_keywords = ["latest", "current", "news", "today", "recent",
                    "search", "find", "what is", "who is", "how to"]

    has_doc_signal = any(kw in query for kw in doc_keywords)
    has_web_signal = any(kw in query for kw in web_keywords)

    if has_doc_signal:
        plan.append("document")
    if has_web_signal:
        plan.append("web")
    if not plan:
        plan = ["document", "web"]

    plan.append("synthesis")

    log_msg = f"[Coordinator] Query: '{state['query']}' → Plan: {plan}"

    return {
        "agent_plan": plan,
        "agent_logs": [log_msg],
    }