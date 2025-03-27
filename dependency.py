from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from user.jwt_auth import JWTAuth, JWTBearer
from user.models import Users
from database import get_db

jwt_auth = JWTAuth()


async def get_current_user(
        token: str = Depends(JWTBearer(jwt_auth)),
        db: AsyncSession = Depends(get_db)
) -> Users:
    payload = jwt_auth.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token or token expired")

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token missing user ID")

    result = await db.execute(select(Users).where(Users.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


async def get_current_staff_user(user: Users = Depends(get_current_user)) -> Users:
    if not user.status:
        raise HTTPException(status_code=403, detail="You do not have permission")
    return user
