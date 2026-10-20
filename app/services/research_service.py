from sqlalchemy.orm import Session

from app.ai.graph import research_graph
from app.models.research import ResearchJob
from app.schemas.research import ResearchCreate


def create_research_job(db: Session, payload: ResearchCreate) -> ResearchJob:
    job = ResearchJob(
        topic=payload.topic.strip(),
        audience=payload.audience.strip() if payload.audience else None,
        depth=payload.depth,
        status="running",
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        initial_state = {
            "topic": job.topic,
            "audience": job.audience or "General audience",
            "depth": job.depth,
            "research_questions": [],
            "search_queries": [],
            "search_results": [],
            "sources": [],
            "coverage_score": 0,
            "feedback": "",
            "report_markdown": "",
            "iteration": 0,
            "max_iterations": 3,
            "additional_queries": [],
        }

        result = research_graph.invoke(initial_state)

        job.report_markdown = result["report_markdown"]
        job.sources = result["sources"]
        job.status = "completed"
        job.error_message = None

        db.commit()
        db.refresh(job)

    except Exception:
        db.rollback()

        job = db.get(ResearchJob, job.id)

        if job is not None:
            job.status = "failed"
            job.error_message = "Research execution failed."
            db.commit()
            db.refresh(job)

        raise

    return job