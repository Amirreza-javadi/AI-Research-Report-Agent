from langgraph.graph import END, START, StateGraph

from app.ai.state import ResearchState
from app.ai.nodes.planner import plan_research
from app.ai.nodes.researcher import researcher_node
from app.ai.nodes.evaluator import evaluator_node
from app.ai.nodes.report_writer import report_writer_node


def route_after_evaluation(state: ResearchState) -> str:
    if state["coverage_score"] >= 80:
        return "finish"

    if state["iteration"] >= state["max_iterations"]:
        return "finish"

    if not state["additional_queries"]:
        return "finish"

    return "research"


def build_research_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("planner", plan_research)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("evaluator", evaluator_node)
    workflow.add_node("report_writer", report_writer_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "evaluator")

    workflow.add_conditional_edges(
        "evaluator",
        route_after_evaluation,
        {
            "research": "researcher",
            "finish": "report_writer",
        },
    )


    workflow.add_edge("report_writer", END)

    return workflow.compile()


research_graph = build_research_graph()
