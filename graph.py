"""
LangGraph Workflow — wires all agents together.

Flow: START → Coordinator → [Document, Web] → Synthesis → END
"""

from langgraph.graph import StateGraph, START, END

from state import AgentState
from agents.coordinator import coordinator_node
from agents.document_agent import document_agent_node
from agents.web_agent import web_agent_node
from agents.synthesis_agent import synthesis_agent_node
from utils.error_handler import safe_node


def route_after_coordinator(state: AgentState) -> str:
    """Decide which agent to call first based on the plan."""
    plan = state.get("agent_plan", [])

    if "document" in plan:
        return "document_agent"
    elif "web" in plan:
        return "web_agent"
    else:
        return "synthesis_agent"


def route_after_document(state: AgentState) -> str:
    """After document agent, check if web agent is also needed."""
    plan = state.get("agent_plan", [])

    if "web" in plan:
        return "web_agent"
    else:
        return "synthesis_agent"


def build_graph():
    """Build and compile the research assistant graph."""

    # Create graph with our state schema
    graph = StateGraph(AgentState)

    # Register all agent nodes
   graph.add_node("coordinator", safe_node(coordinator_node, "Coordinator"))
    graph.add_node("document_agent", safe_node(document_agent_node, "Document Agent"))
    graph.add_node("web_agent", safe_node(web_agent_node, "Web Agent"))
    graph.add_node("synthesis_agent", safe_node(synthesis_agent_node, "Synthesis Agent"))
    # Entry point
    graph.add_edge(START, "coordinator")

    # Coordinator routes to the right agent
    graph.add_conditional_edges(
        "coordinator",
        route_after_coordinator,
        {
            "document_agent": "document_agent",
            "web_agent": "web_agent",
            "synthesis_agent": "synthesis_agent",
        }
    )

    # After document agent, maybe go to web or straight to synthesis
    graph.add_conditional_edges(
        "document_agent",
        route_after_document,
        {
            "web_agent": "web_agent",
            "synthesis_agent": "synthesis_agent",
        }
    )

    # Web agent always goes to synthesis
    graph.add_edge("web_agent", "synthesis_agent")

    # Synthesis is the end
    graph.add_edge("synthesis_agent", END)

    # Compile and return
    return graph.compile()

