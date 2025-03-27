from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID

import uuid
from database import Base


class Worker(Base):
    __tablename__ = "worker"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    media = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


