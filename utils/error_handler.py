"""
Error handler wrapper for agent nodes.
Catches exceptions so one agent failing doesn't crash the whole pipeline.
"""


def safe_node(node_fn, node_name: str):
    """
    Wrap an agent node function with error handling.
    If the node crashes, log the error and return empty results.
    """
    def wrapper(state):
        try:
            return node_fn(state)
        except Exception as e:
            error_msg = f"[{node_name}] Error: {str(e)}"
            print(f"  ⚠️ {error_msg}")
            return {
                "agent_logs": [error_msg],
            }

    return wrapper