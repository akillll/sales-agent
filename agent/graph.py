from langgraph.graph import StateGraph
from agent.nodes import (
    enrich_node,
    email_node,
    classify_reply_node,
    objection_node,
    positive_node,
    neutral_node,
    route_reply
)
from agent.state import AgentState

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("enrich", enrich_node)
    graph.add_node("email", email_node)
    graph.add_node("classify", classify_reply_node)
    graph.add_node("objection", objection_node)
    graph.add_node("positive", positive_node)
    graph.add_node("neutral", neutral_node)

    graph.set_entry_point("enrich")

    graph.add_edge("enrich", "email")
    graph.add_edge("email", "classify")
    
    graph.add_conditional_edges(
        "classify",
        route_reply,
        {
            "objection": "objection",
            "positive": "positive",
            "neutral": "neutral",
            "no_reply": "__end__",
        }
    )

    return graph.compile()