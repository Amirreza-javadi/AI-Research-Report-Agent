from app.ai.state import ResearchState
from app.ai.tools.web_searche import web_search


def researcher_node(state: ResearchState) -> dict:
    """Search the web and accumulate unique results across research iterations."""

    if state["iteration"] == 0:
        queries = state["search_queries"]
    else:
        queries = state["additional_queries"]

    queries = list(dict.fromkeys(
        query.strip()
        for query in queries
        if query.strip()
    ))[:8]

    if not queries:
        return {
            "search_results": state["search_results"],
            "sources": state["sources"],
        }

    all_results = list(state["search_results"])
    seen_urls = {
        result.get("url", "")
        for result in all_results
        if result.get("url")
    }

    failed_queries = []

    for query in queries:
        try:
            results = web_search(query)
        except Exception as exc:
            failed_queries.append(query)
            print(f"Warning: Search failed for query: {query}")
            continue

        for result in results:
            url = result.get("url", "")

            if not url or url in seen_urls:
                continue

            seen_urls.add(url)
            all_results.append({
                **result,
                "query": query,
            })

    sources_by_url = {
        source["url"]: source
        for source in state["sources"]
        if source.get("url")
    }

    for result in all_results:
        sources_by_url[result["url"]] = {
            "title": result.get("title", ""),
            "url": result["url"],
        }

    return {
        "search_results": all_results,
        "sources": list(sources_by_url.values()),
    }
