from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.research import ResearchJob
from app.schemas.research import ResearchCreate, ResearchList, ResearchRead
from app.services.research_service import create_research_job

router = APIRouter()


@router.post("", response_model=ResearchRead, status_code=status.HTTP_201_CREATED)
def create_research(
    payload: ResearchCreate,
    db: Session = Depends(get_db),
) -> ResearchRead:
    return create_research_job(db, payload)


@router.get("", response_model=ResearchList)
def list_research(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> ResearchList:
    total = db.scalar(select(func.count()).select_from(ResearchJob)) or 0
    jobs = db.scalars(
        select(ResearchJob).order_by(ResearchJob.created_at.desc()).limit(limit).offset(offset)
    ).all()
    return ResearchList(items=list(jobs), total=total, limit=limit, offset=offset)


@router.get("/{research_id}", response_model=ResearchRead)
def get_research(research_id: int, db: Session = Depends(get_db)) -> ResearchRead:
    job = db.get(ResearchJob, research_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Research job not found")
    return job
