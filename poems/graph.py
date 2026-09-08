from typing import Literal

from langgraph.graph import END, START, StateGraph

from poems.nodes import check_draft, revise_draft, write_draft
from poems.state import PoemState

MAX_REVISIONS = 2


def route_after_check(state: PoemState) -> Literal["revise", "finish"]:
    if not state["validation_errors"]:
        return "finish"

    if state["revision_count"] >= MAX_REVISIONS:
        return "finish"

    return "revise"


def build_graph():
    builder = StateGraph(PoemState)

    builder.add_node("write_draft", write_draft)
    builder.add_node("check_draft", check_draft)
    builder.add_node("revise_draft", revise_draft)

    builder.add_edge(START, "write_draft")
    builder.add_edge("write_draft", "check_draft")

    builder.add_conditional_edges(
        "check_draft",
        route_after_check,
        {
            "revise": "revise_draft",
            "finish": END,
        },
    )

    builder.add_edge("revise_draft", "check_draft")

    return builder.compile()
