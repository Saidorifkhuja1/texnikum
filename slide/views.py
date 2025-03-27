import os
from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from .schemas import SlideCreate, SlideUpdate, SlideResponse
from .models import Slide
from dependency import get_current_staff_user
from user.models import Users
from sqlalchemy.future import select
import shutil

router = APIRouter()

UPLOAD_FOLDER = "media/slides"


@router.post("/{create_slide}", response_model=SlideResponse, status_code=201)
async def create_slide(
    title: str = Form(...),
    body: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_staff_user),
):
    media_path = None
    if media:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_location = os.path.join(UPLOAD_FOLDER, media.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        media_path = file_location

    slide = Slide(title=title, body=body, media=media_path)
    db.add(slide)
    await db.commit()
    await db.refresh(slide)
    return slide


@router.get("/{get_all_slides}", response_model=list[SlideResponse])
async def get_all_slides(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Slide))
    return result.scalars().all()


@router.get("/{slide_by_id}", response_model=SlideResponse)
async def get_slide(slide_id: UUID, db: AsyncSession = Depends(get_db)):
    slide = await db.get(Slide, slide_id)
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")
    return slide


@router.put("/{slide_id}", response_model=SlideResponse)
async def update_slide(
    slide_id: UUID,
    title: str = Form(...),
    body: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_staff_user),
):
    slide = await db.get(Slide, slide_id)
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")

    slide.title = title
    slide.body = body

    if media:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file_location = os.path.join(UPLOAD_FOLDER, media.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        slide.media = file_location

    await db.commit()
    await db.refresh(slide)
    return slide


@router.delete("/{slide_id}", status_code=204)
async def delete_slide(
    slide_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: Users = Depends(get_current_staff_user),
):
    slide = await db.get(Slide, slide_id)
    if not slide:
        raise HTTPException(status_code=404, detail="Slide not found")
    await db.delete(slide)
    await db.commit()
