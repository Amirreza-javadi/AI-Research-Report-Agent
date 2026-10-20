from unittest.mock import patch

from app.ai.graph import research_graph
from app.ai.nodes.planner import ResearchPlan
from app.ai.nodes.evaluator import ResearchEvaluation


@patch("app.ai.nodes.report_writer.report_chain")
@patch("app.ai.nodes.evaluator.evaluation_chain")
@patch("app.ai.nodes.researcher.web_search")
@patch("app.ai.nodes.planner.planner_chain")
def test_research_graph_end_to_end(
    mock_planner,
    mock_search,
    mock_evaluator,
    mock_report,
):
    # 1. Mock planner
    mock_planner.invoke.return_value = ResearchPlan(
        research_questions=[
            "What are AI agents?",
            "What are their limitations?",
            "How are AI agents used?",
        ],
        search_queries=[
            "AI agents architecture",
            "AI agent limitations",
            "AI agent applications",
        ],
    )

    # 2. Mock web search
    mock_search.return_value = [
        {
            "title": "AI Agents Guide",
            "url": "https://example.com/agents",
            "content": "AI agents can plan and execute tasks.",
        }
    ]

   # 3. Mock evaluator
    mock_evaluator.invoke.return_value = ResearchEvaluation(
        coverage_score=90,
        feedback="The research covers the main questions.",
        additional_queries=[],
    )

    # 4. Mock report writer
    mock_report.invoke.return_value.content = (
        "# AI Agents Research Report\n\n"
        "## Executive Summary\n\n"
        "AI agents can plan and execute tasks."
    )

    # 5. Initial graph state
    initial_state = {
        "topic": "AI Agents",
        "audience": "Software developers",
        "depth": "detailed",
        "research_questions": [],
        "search_queries": [],
        "additional_queries": [],
        "search_results": [],
        "sources": [],
        "coverage_score": 0,
        "feedback": "",
        "report_markdown": "",
        "iteration": 0,
        "max_iterations": 3,
    }

    # 6. Run graph
    result = research_graph.invoke(initial_state)

    # 7. Verify final output
    assert result["research_questions"] == [
        "What are AI agents?",
        "What are their limitations?",
        "How are AI agents used?",
    ]

    assert result["coverage_score"] == 90
    assert len(result["search_results"]) == 1
    assert len(result["sources"]) == 1

    assert result["report_markdown"].startswith(
        "# AI Agents Research Report"
    )

    mock_planner.invoke.assert_called_once()
    assert mock_search.call_count == 3

    mock_search.assert_any_call("AI agents architecture")
    mock_search.assert_any_call("AI agent limitations")
    mock_search.assert_any_call("AI agent applications")

    mock_evaluator.invoke.assert_called_once()
    mock_report.invoke.assert_called_once()
