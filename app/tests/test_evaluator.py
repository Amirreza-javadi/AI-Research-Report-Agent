from unittest.mock import patch

from app.ai.nodes.evaluator import evaluator_node, ResearchEvaluation


def make_state():
    return {
        "topic": "AI Agents",
        "audience": "Developers",
        "depth": "detailed",
        "research_questions": [
            "What are AI agents?",
            "What are their limitations?",
        ],
        "search_queries": [
            "AI agents architecture",
        ],
        "additional_queries": [],
        "search_results": [
            {
                "title": "AI Agents Guide",
                "url": "https://example.com/agents",
                "content": "An introduction to AI agents.",
            }
        ],
        "sources": [],
        "coverage_score": 0,
        "feedback": "",
        "report_markdown": "",
        "iteration": 0,
        "max_iterations": 3,
    }


@patch("app.ai.nodes.evaluator.evaluation_chain")
def test_evaluator_returns_coverage_and_feedback(mock_chain):
    mock_chain.invoke.return_value = ResearchEvaluation(
        coverage_score=85,
        feedback="The research covers most questions.",
        additional_queries=[],
    )

    result = evaluator_node(make_state())

    assert result["coverage_score"] == 85
    assert result["feedback"] == "The research covers most questions."
    assert result["additional_queries"] == []
    assert result["iteration"] == 1

    mock_chain.invoke.assert_called_once()


@patch("app.ai.nodes.evaluator.evaluation_chain")
def test_evaluator_adds_new_queries(mock_chain):
    mock_chain.invoke.return_value = ResearchEvaluation(
        coverage_score=60,
        feedback="More information about limitations is needed.",
        additional_queries=[
            "AI agent limitations",
            "AI agent security risks",
        ],
    )

    result = evaluator_node(make_state())

    assert result["additional_queries"] == [
        "AI agent limitations",
        "AI agent security risks",
    ]

    assert result["search_queries"] == [
        "AI agents architecture",
        "AI agent limitations",
        "AI agent security risks",
    ]

    mock_chain.invoke.assert_called_once()


@patch("app.ai.nodes.evaluator.evaluation_chain")
def test_evaluator_removes_duplicate_queries(mock_chain):
    mock_chain.invoke.return_value = ResearchEvaluation(
        coverage_score=70,
        feedback="Some gaps remain.",
        additional_queries=[
            "AI agents architecture",
            "AI agent limitations",
            "AI agent limitations",
            "  AI agent security risks  ",
            "",
        ],
    )

    result = evaluator_node(make_state())

    assert result["additional_queries"] == [
        "AI agent limitations",
        "AI agent security risks",
    ]

    assert result["search_queries"] == [
        "AI agents architecture",
        "AI agent limitations",
        "AI agent security risks",
    ]

    mock_chain.invoke.assert_called_once()


@patch("app.ai.nodes.evaluator.evaluation_chain")
def test_evaluator_increments_iteration(mock_chain):
    mock_chain.invoke.return_value = ResearchEvaluation(
        coverage_score=75,
        feedback="More research is recommended.",
        additional_queries=["AI agent evaluation methods"],
    )

    state = make_state()
    state["iteration"] = 2

    result = evaluator_node(state)

    assert result["iteration"] == 3

    mock_chain.invoke.assert_called_once()