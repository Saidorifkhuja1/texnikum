from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime


class WorkerBase(BaseModel):
    name: str
    description: str


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class WorkerRead(WorkerBase):
    id: UUID
    media: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


