from fastapi import APIRouter

from app.api.routes.research import router as research_router

api_router = APIRouter()
api_router.include_router(research_router, prefix="/research", tags=["research"])
