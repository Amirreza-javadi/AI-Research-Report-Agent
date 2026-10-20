from unittest.mock import patch

from app.ai.state import ResearchState


def mock_research_result() -> dict:
    return {
        "topic": "How adaptive research agents work",
        "audience": "software developers",
        "depth": "standard",
        "research_questions": [
            "What are adaptive research agents?",
            "How do they search for information?",
            "How do they evaluate research quality?",
        ],
        "search_queries": ["adaptive research agents"],
        "search_results": [
            {
                "title": "Adaptive Research Agents",
                "url": "https://example.com/research-agents",
                "content": "Adaptive agents improve research iteratively.",
                "score": 0.95,
            }
        ],
        "sources": [
            {
                "title": "Adaptive Research Agents",
                "url": "https://example.com/research-agents",
            }
        ],
        "coverage_score": 90,
        "feedback": "Research coverage is sufficient.",
        "report_markdown": (
            "# Adaptive Research Agents\n\n"
            "Adaptive agents improve research iteratively."
        ),
        "iteration": 1,
        "max_iterations": 3,
        "additional_queries": [],
    }


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@patch("app.services.research_service.research_graph.invoke")
def test_create_and_get_research(mock_invoke, client):
    mock_invoke.return_value = mock_research_result()

    create_response = client.post(
        "/api/v1/research",
        json={
            "topic": "How adaptive research agents work",
            "audience": "software developers",
            "depth": "standard",
        },
    )

    assert create_response.status_code == 201

    created = create_response.json()

    assert created["topic"] == "How adaptive research agents work"
    assert created["status"] == "completed"
    assert created["id"] > 0
    assert created["report_markdown"].startswith("# Adaptive Research Agents")
    assert len(created["sources"]) == 1

    get_response = client.get(f"/api/v1/research/{created['id']}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == created["id"]
    mock_invoke.assert_called_once()


@patch("app.services.research_service.research_graph.invoke")
def test_list_research(mock_invoke, client):
    mock_invoke.return_value = mock_research_result()

    first_response = client.post(
        "/api/v1/research",
        json={"topic": "First research topic"},
    )
    second_response = client.post(
        "/api/v1/research",
        json={"topic": "Second research topic"},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201

    response = client.get("/api/v1/research?limit=1&offset=0")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 1
    assert mock_invoke.call_count == 2


def test_invalid_topic_is_rejected(client):
    response = client.post(
        "/api/v1/research",
        json={"topic": "x"},
    )

    assert response.status_code == 422