"""
State definition for the Agentic Research Assistant.

This is the shared state that flows through every node in the LangGraph.
Think of it as the "memory" that all agents can read from and write to.
"""

from typing import TypedDict, Annotated
from operator import add


class AgentState(TypedDict):
    """
    Every node receives this state and returns a partial update.
    LangGraph merges the update into the existing state automatically.
    """
    query: str                              # user's current question
    chat_history: list[dict]                # previous (query, answer) pairs
    doc_results: list[dict]                 # chunks retrieved from PDFs
    web_results: list[dict]                 # results from web search
    agent_plan: list[str]                   # which agents to call
    final_answer: str                       # the synthesized response
    sources: list[dict]                     # sources used (doc names, URLs)
    agent_logs: Annotated[list[str], add]   # step-by-step log (append-only)