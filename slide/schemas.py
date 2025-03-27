from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SlideCreate(BaseModel):
    title: str
    body: str


class SlideUpdate(BaseModel):
    title: str
    body: str


class SlideResponse(BaseModel):
    id: UUID
    title: str
    body: str
    media: str | None = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
