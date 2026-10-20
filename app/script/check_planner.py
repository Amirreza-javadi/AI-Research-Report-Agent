from pprint import pprint

from app.ai.nodes.planner import plan_research


def main() -> None:
    state = {
        "topic": "The impact of AI agents on software development",
        "audience": "Software developers and technical managers",
        "depth": "detailed",
    }

    print("Generating research plan...\n")

    result = plan_research(state)

    print("Research Questions:")
    pprint(result["research_questions"])

    print("\nSearch Queries:")
    pprint(result["search_queries"])

    print("\nPlanner completed successfully!")


if __name__ == "__main__":
    main()