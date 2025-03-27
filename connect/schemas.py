from pydantic import BaseModel, UUID4
from typing import Optional


class ConnectBase(BaseModel):
    name: str
    family_name: str
    comment: Optional[str] = None
    phone: str


class ConnectCreate(ConnectBase):
    pass


class ConnectOut(ConnectBase):
    id: UUID4

    class Config:
        from_attributes = True
