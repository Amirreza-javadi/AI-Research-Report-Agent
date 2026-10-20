from app.ai.graph import research_graph


def main():
    initial_state = {
        "topic": "The impact of AI agents on software development",
        "audience": "Software developers and technical managers",
        "depth": "detailed",
        "additional_queries": [],
        "research_questions": [],
        "search_queries": [],
        "search_results": [],
        "sources": [],
        "coverage_score": 0,
        "feedback": "",
        "report_markdown": "",
        "iteration": 0,
        "max_iterations": 3,
    }

    result = research_graph.invoke(initial_state)

    print("\n=== RESEARCH QUESTIONS ===")
    for question in result["research_questions"]:
        print("-", question)

    print("\n=== SOURCES ===")
    for source in result["sources"]:
        print(f"- {source['title']}: {source['url']}")

    print(f"\nTotal search results: {len(result['search_results'])}")
    print(f"\nCoverage Score: {result['coverage_score']}/100")
    print(f"Iterations: {result['iteration']}")

    print("\n=== FINAL RESEARCH REPORT ===")
    print(result["report_markdown"])


if __name__ == "__main__":
    main()
