from typing import Any, TypedDict


class ResearchState(TypedDict):
    # Original request
    topic: str
    audience: str
    depth: str

    # Research planning
    research_questions: list[str]
    search_queries: list[str]

    # Collected information
    search_results: list[dict[str, Any]]
    sources: list[dict[str, str]]

    # Evaluation and report
    coverage_score: int
    feedback: str
    report_markdown: str

    # Loop control
    iteration: int
    max_iterations: int
    
    additional_queries: list[str]
