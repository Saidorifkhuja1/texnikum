from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class NewsBase(BaseModel):
    title: str
    body: str

class NewsCreate(NewsBase):
    pass

class NewsUpdate(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None

class NewsRead(NewsBase):
    id: UUID
    media: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
