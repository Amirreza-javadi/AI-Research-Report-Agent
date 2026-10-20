from unittest.mock import patch

from app.ai.nodes.researcher import researcher_node


def make_state():
    return {
        "topic": "AI Agents",
        "audience": "Developers",
        "depth": "detailed",
        "research_questions": [],
        "search_queries": ["AI agents architecture"],
        "additional_queries": [],
        "search_results": [],
        "sources": [],
        "coverage_score": 0,
        "feedback": "",
        "report_markdown": "",
        "iteration": 0,
        "max_iterations": 3,
    }


@patch("app.ai.nodes.researcher.web_search")
def test_researcher_collects_results(mock_search):
    mock_search.return_value = [
        {
            "title": "AI Agents Guide",
            "url": "https://example.com/agents",
            "content": "An introduction to AI agents.",
        }
    ]

    result = researcher_node(make_state())

    assert len(result["search_results"]) == 1
    assert result["search_results"][0]["title"] == "AI Agents Guide"
    assert len(result["sources"]) == 1
    mock_search.assert_called_once_with("AI agents architecture")


@patch("app.ai.nodes.researcher.web_search")
def test_researcher_deduplicates_urls(mock_search):
    mock_search.return_value = [
        {
            "title": "AI Agents Guide",
            "url": "https://example.com/agents",
            "content": "First result.",
        },
        {
            "title": "Duplicate page",
            "url": "https://example.com/agents",
            "content": "Duplicate result.",
        },
    ]

    result = researcher_node(make_state())

    assert len(result["search_results"]) == 1
    assert len(result["sources"]) == 1


@patch("app.ai.nodes.researcher.web_search")
def test_researcher_preserves_existing_results(mock_search):
    state = make_state()
    state["iteration"] = 1
    state["additional_queries"] = ["AI agent limitations"]
    state["search_results"] = [
        {
            "title": "Existing result",
            "url": "https://example.com/existing",
            "content": "Already collected.",
        }
    ]
    state["sources"] = [
        {
            "title": "Existing result",
            "url": "https://example.com/existing",
        }
    ]

    mock_search.return_value = [
        {
            "title": "New result",
            "url": "https://example.com/new",
            "content": "New information.",
        },
        {
            "title": "Existing result again",
            "url": "https://example.com/existing",
            "content": "Duplicate of old information.",
        },
    ]

    result = researcher_node(state)

    assert len(result["search_results"]) == 2
    assert len(result["sources"]) == 2
    assert result["search_results"][0]["title"] == "Existing result"
    assert result["search_results"][1]["title"] == "New result"
    mock_search.assert_called_once_with("AI agent limitations")


@patch("app.ai.nodes.researcher.web_search")
def test_researcher_continues_after_search_failure(mock_search):
    mock_search.side_effect = [
        RuntimeError("Temporary search failure"),
        [
            {
                "title": "Successful result",
                "url": "https://example.com/success",
                "content": "Useful research information.",
            }
        ],
    ]

    state = make_state()
    state["search_queries"] = [
        "Failing query",
        "Successful query",
    ]

    result = researcher_node(state)

    assert len(result["search_results"]) == 1
    assert result["search_results"][0]["title"] == "Successful result"
    assert mock_search.call_count == 2
