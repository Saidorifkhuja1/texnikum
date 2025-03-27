from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
import shutil
import os

from database import get_db
from .models import News
from .schemas import NewsCreate, NewsUpdate, NewsRead
from dependency import get_current_staff_user

router = APIRouter()

MEDIA_DIR = "media/news"
os.makedirs(MEDIA_DIR, exist_ok=True)

@router.post("/{create_news}", response_model=NewsRead, status_code=201)
async def create_news(
    title: str = Form(...),
    body: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    media_path = None
    if media:
        file_ext = os.path.splitext(media.filename)[1]
        file_name = f"{title.replace(' ', '_')}_{media.filename}"
        media_path = os.path.join(MEDIA_DIR, file_name)
        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        media_path = "/" + media_path

    new_news = News(title=title, body=body, media=media_path)
    db.add(new_news)
    await db.commit()
    await db.refresh(new_news)
    return new_news

@router.get("/{get_all_news}", response_model=list[NewsRead])
async def get_all_news(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News))
    return result.scalars().all()

@router.get("/{news_by_id}", response_model=NewsRead)
async def get_news(news_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    return news

@router.put("/{news_id}", response_model=NewsRead)
async def update_news(
    news_id: UUID,
    title: str = Form(...),
    body: str = Form(...),
    media: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar_one_or_none()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")

    news.title = title
    news.body = body

    if media:
        file_name = f"{title.replace(' ', '_')}_{media.filename}"
        media_path = os.path.join(MEDIA_DIR, file_name)
        with open(media_path, "wb") as buffer:
            shutil.copyfileobj(media.file, buffer)
        news.media = "/" + media_path

    await db.commit()
    await db.refresh(news)
    return news

@router.delete("/{news_id}", status_code=204)
async def delete_news(
    news_id: UUID,
    db: AsyncSession = Depends(get_db),
    staff_user=Depends(get_current_staff_user),
):
    result = await db.execute(select(News).where(News.id == news_id))
    news = result.scalar()
    if not news:
        raise HTTPException(status_code=404, detail="News not found")
    await db.delete(news)
    await db.commit()

