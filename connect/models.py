from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base


class Connect(Base):
    __tablename__ = "connect"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    name = Column(String(100), nullable=False)
    family_name = Column(String(100), nullable=False)
    comment = Column(String(500), nullable=True)
    phone = Column(String(20), nullable=False)
