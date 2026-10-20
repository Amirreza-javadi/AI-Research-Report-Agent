from unittest.mock import patch, MagicMock

import pytest

from app.ai.nodes.report_writer import report_writer_node


def make_state():
    return {
        "topic": "AI Agents",
        "audience": "Developers",
        "depth": "detailed",
        "research_questions": [
            "What are AI agents?",
            "What are their limitations?",
        ],
        "search_queries": ["AI agents architecture"],
        "additional_queries": [],
        "search_results": [
            {
                "title": "AI Agents Guide",
                "url": "https://example.com/agents",
                "content": "An introduction to AI agents.",
            }
        ],
        "sources": [
            {
                "title": "AI Agents Guide",
                "url": "https://example.com/agents",
            }
        ],
        "coverage_score": 85,
        "feedback": "The research covers most questions.",
        "report_markdown": "",
        "iteration": 1,
        "max_iterations": 3,
    }


@patch("app.ai.nodes.report_writer.report_chain")
def test_report_writer_generates_markdown(mock_chain):
    mock_response = MagicMock()
    mock_response.content = "# AI Agents\n\n## Executive Summary\n\nAI agents ..."
    mock_chain.invoke.return_value = mock_response

    result = report_writer_node(make_state())

    assert result["report_markdown"].startswith("# AI Agents")
    assert "Executive Summary" in result["report_markdown"]
    mock_chain.invoke.assert_called_once()


@patch("app.ai.nodes.report_writer.report_chain")
def test_report_writer_passes_research_data_to_chain(mock_chain):
    mock_response = MagicMock()
    mock_response.content = "# Research Report"
    mock_chain.invoke.return_value = mock_response

    state = make_state()
    report_writer_node(state)

    inputs = mock_chain.invoke.call_args.args[0]

    assert inputs["topic"] == "AI Agents"
    assert inputs["audience"] == "Developers"
    assert inputs["coverage_score"] == 85
    assert "What are AI agents?" in inputs["research_questions"]
    assert "AI Agents Guide" in inputs["search_results"]
    assert "https://example.com/agents" in inputs["sources"]


@patch("app.ai.nodes.report_writer.report_chain")
def test_report_writer_uses_default_feedback_when_empty(mock_chain):
    mock_response = MagicMock()
    mock_response.content = "# Research Report"
    mock_chain.invoke.return_value = mock_response

    state = make_state()
    state["feedback"] = ""

    report_writer_node(state)

    inputs = mock_chain.invoke.call_args.args[0]

    assert inputs["feedback"] == "No additional feedback."


def test_report_writer_raises_error_without_search_results():
    state = make_state()
    state["search_results"] = []

    with pytest.raises(
        ValueError,
        match="Cannot generate a research report without search results.",
    ):
        report_writer_node(state)