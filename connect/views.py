from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from database import get_db
from .models import Connect
from .schemas import ConnectCreate, ConnectOut
from dependency import get_current_staff_user

router = APIRouter()



@router.post("/", response_model=ConnectOut)
async def create_connect(data: ConnectCreate, db: AsyncSession = Depends(get_db)):
    connect_entry = Connect(**data.dict())
    db.add(connect_entry)
    await db.commit()
    await db.refresh(connect_entry)
    return connect_entry



@router.get("/", response_model=List[ConnectOut])
async def list_connects(db: AsyncSession = Depends(get_db), staff=Depends(get_current_staff_user)):
    result = await db.execute(select(Connect))
    return result.scalars().all()



@router.delete("/{connect_id}")
async def delete_connect(connect_id: UUID, db: AsyncSession = Depends(get_db),
                         staff=Depends(get_current_staff_user)):
    connect_entry = await db.get(Connect, connect_id)
    if not connect_entry:
        raise HTTPException(status_code=404, detail="Connect request not found")

    await db.delete(connect_entry)
    await db.commit()
    return {"message": "Connect request deleted successfully"}
