from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

from app.ai.state import ResearchState

load_dotenv()

class ResearchEvaluation(BaseModel):
    coverage_score: int = Field(
        ge=0,
        le=100,
        description="How completely the research questions are covered.",
    )

    feedback: str = Field(
        description="Missing information and remaining research gaps.",
    )

    additional_queries: list[str] = Field(
        max_length=5,
        description="New search queries addressing important gaps.",
    )


evaluation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an expert research quality evaluator.

            Evaluate how well the collected search results
            answer the research questions.

            Consider relevance, coverage, diversity, and
            important information gaps.

            Return a coverage score from 0 to 100.
            Suggest up to 5 new search queries only when
            important gaps remain.

            Avoid duplicate or already-used queries.
            Do not claim that search snippets prove factual accuracy.
            """,
        ),
        (
            "human",
            """
            Topic: {topic}

            Research questions:
            {research_questions}

            Search results:
            {search_results}

            Previously identified gaps:
            {feedback}
            """,
        ),
    ]
)


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

structured_evaluator = llm.with_structured_output(
    ResearchEvaluation,
    method="json_schema",
    strict=True,
)

evaluation_chain = evaluation_prompt | structured_evaluator


def evaluator_node(state: ResearchState) -> dict:
    results = state["search_results"][:20]

    formatted_results = "\n\n".join(
        (
            f"Title: {item.get('title', '')}\n"
            f"URL: {item.get('url', '')}\n"
            f"Content: {item.get('content', '')[:800]}"
        )
        for item in results
    )

    evaluation = evaluation_chain.invoke(
        {
            "topic": state["topic"],
            "research_questions": "\n".join(
                state["research_questions"]
            ),
            "search_results": formatted_results,
            "feedback": state["feedback"],
        }
    )

    existing_queries = {
        query.strip().casefold()
        for query in state["search_queries"]
    }

    new_queries = []
    seen_queries = set(existing_queries)

    for query in evaluation.additional_queries:
        cleaned_query = query.strip()
        normalized_query = cleaned_query.casefold()

        if cleaned_query and normalized_query not in seen_queries:
            new_queries.append(cleaned_query)
            seen_queries.add(normalized_query)

    return {
        "coverage_score": evaluation.coverage_score,
        "feedback": evaluation.feedback,
        "additional_queries": new_queries,
        "search_queries": state["search_queries"] + new_queries,
        "iteration": state["iteration"] + 1,
    }
