from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ResearchCreate(BaseModel):
    topic: str = Field(min_length=3, max_length=500, description="Question or topic to research")
    audience: str | None = Field(default=None, max_length=250)
    depth: Literal["quick", "standard", "deep"] = "standard"


class ResearchRead(BaseModel):
    id: int
    topic: str
    audience: str | None
    depth: str
    status: str
    report_markdown: str | None
    sources: list | None
    error_message: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResearchList(BaseModel):
    items: list[ResearchRead]
    total: int
    limit: int
    offset: int
