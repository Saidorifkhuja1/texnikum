from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
import shutil
import os

from database import get_db
from .models import Worker
from .schemas import WorkerCreate, WorkerUpdate, WorkerRead
from dependency import get_current_staff_user

router = APIRouter()

WORKER_MEDIA_DIR = "media/worker"
os.makedirs(WORKER_MEDIA_DIR, exist_ok=True)

@router.post("/", response_model=WorkerRead, status_code=201)
async def create_worker(
    name: str = Form(...),
    description: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    media_path = None
    if media:
        file_name = f"{name.replace(' ', '_')}_{media.filename}"
        media_path = os.path.join(WORKER_MEDIA_DIR, file_name)
        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        media_path = "/" + media_path

    worker = Worker(name=name, description=description, media=media_path)
    db.add(worker)
    await db.commit()
    await db.refresh(worker)
    return worker

@router.get("/", response_model=list[WorkerRead])
async def list_workers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Worker))
    return result.scalars().all()

@router.get("/{worker_id}", response_model=WorkerRead)
async def get_worker(worker_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Worker).where(Worker.id == worker_id))
    worker = result.scalar()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker

@router.put("/{worker_id}", response_model=WorkerRead)
async def update_worker(
    worker_id: UUID,
    name: str = Form(...),
    description: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    result = await db.execute(select(Worker).where(Worker.id == worker_id))
    worker = result.scalar_one_or_none()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    worker.name = name
    worker.description = description

    if media:
        file_name = f"{name.replace(' ', '_')}_{media.filename}"
        media_path = os.path.join(WORKER_MEDIA_DIR, file_name)
        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        worker.media = "/" + media_path

    await db.commit()
    await db.refresh(worker)
    return worker

@router.delete("/{worker_id}", status_code=204)
async def delete_worker(
    worker_id: UUID,
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    result = await db.execute(select(Worker).where(Worker.id == worker_id))
    worker = result.scalar_one_or_none()
    if not worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    await db.delete(worker)
    await db.commit()


