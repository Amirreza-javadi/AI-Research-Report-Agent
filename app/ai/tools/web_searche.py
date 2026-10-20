from tavily import TavilyClient

from app.core.config import settings


tavily_client = TavilyClient(
    api_key=settings.tavily_api_key,
)


def web_search(query: str) -> list[dict]:
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=3,
    )

    return [
        {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "content": item.get("content", ""),
            "score": item.get("score", 0.0),
        }
        for item in response.get("results", [])
    ]
