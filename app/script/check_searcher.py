from app.ai.tools.web_searche import web_search


def main():
    results = web_search(
        "Latest research on AI agents in software development"
    )

    print(f"Number of results: {len(results)}")

    for index, result in enumerate(results, start=1):
        print(f"\n--- Result {index} ---")
        print("Title:", result["title"])
        print("URL:", result["url"])
        print("Content:", result["content"][:250])


if __name__ == "__main__":
    main()
