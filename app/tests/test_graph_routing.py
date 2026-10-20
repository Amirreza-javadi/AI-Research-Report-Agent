from app.ai.graph import route_after_evaluation
from app.ai.state import ResearchState


def make_state(
    coverage_score: int = 50,
    iteration: int = 1,
    max_iterations: int = 3,
    additional_queries: list[str] | None = None,
) -> ResearchState:
    return {
        "topic": "AI Agents",
        "audience": "Developers",
        "depth": "detailed",
        "research_questions": [],
        "search_queries": [],
        "additional_queries": additional_queries or [],
        "search_results": [],
        "sources": [],
        "coverage_score": coverage_score,
        "feedback": "",
        "report_markdown": "",
        "iteration": iteration,
        "max_iterations": max_iterations,
    }


def test_finish_when_coverage_is_sufficient():
    state = make_state(
        coverage_score=85,
        additional_queries=["More research"],
    )

    assert route_after_evaluation(state) == "finish"


def test_finish_when_max_iterations_reached():
    state = make_state(
        coverage_score=60,
        iteration=3,
        max_iterations=3,
        additional_queries=["More research"],
    )

    assert route_after_evaluation(state) == "finish"


def test_finish_when_no_additional_queries():
    state = make_state(
        coverage_score=60,
        additional_queries=[],
    )

    assert route_after_evaluation(state) == "finish"


def test_continue_research_when_coverage_is_low():
    state = make_state(
        coverage_score=60,
        iteration=1,
        max_iterations=3,
        additional_queries=["Research AI agent limitations"],
    )

    assert route_after_evaluation(state) == "research"