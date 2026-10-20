from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from app.ai.state import ResearchState

load_dotenv()

report_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a professional research analyst and report writer.

            Your task is to produce a clear, well-structured,
            evidence-based research report using the supplied sources.

            Follow these rules:
            - Write the report in English.
            - Use Markdown formatting.
            - Start with a descriptive title.
            - Include an Executive Summary.
            - Include clearly organized sections addressing the
              research questions.
            - Explain important findings and their implications.
            - Distinguish supported findings from uncertain claims.
            - Do not invent facts, statistics, quotations, or sources.
            - If the available evidence is insufficient, state this clearly.
            - Include a Limitations section.
            - Finish with a Conclusion.
            - Include a Sources section using the supplied source titles
              and URLs.
            - Only include sources that were actually provided.
            - Do not claim to have verified information beyond the
              supplied search results.
            """,
        ),
        (
            "human",
            """
            Research topic:
            {topic}

            Intended audience:
            {audience}

            Research depth:
            {depth}

            Research questions:
            {research_questions}

            Coverage score:
            {coverage_score}/100

            Evaluator feedback:
            {feedback}

            Collected research results:
            {search_results}

            Source list:
            {sources}

            Write the final research report based on this information.
            """,
        ),
    ]
)


report_llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

report_chain = report_prompt | report_llm


def report_writer_node(state: ResearchState) -> dict:
    """Generate a final Markdown report from the collected research."""

    if not state["search_results"]:
        raise ValueError(
            "Cannot generate a research report without search results."
        )

    formatted_results = "\n\n".join(
        (
            f"Title: {result.get('title', '')}\n"
            f"URL: {result.get('url', '')}\n"
            f"Content: {result.get('content', '')[:1200]}"
        )
        for result in state["search_results"][:20]
    )

    formatted_sources = "\n".join(
        f"- {source['title']}: {source['url']}"
        for source in state["sources"]
    )

    response = report_chain.invoke(
        {
            "topic": state["topic"],
            "audience": state["audience"],
            "depth": state["depth"],
            "research_questions": "\n".join(
                f"- {question}"
                for question in state["research_questions"]
            ),
            "coverage_score": state["coverage_score"],
            "feedback": state["feedback"] or "No additional feedback.",
            "search_results": formatted_results,
            "sources": formatted_sources,
        }
    )

    return {
        "report_markdown": response.content,
    }