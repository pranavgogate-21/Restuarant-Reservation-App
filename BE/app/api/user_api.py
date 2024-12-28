from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.Models.response_builder import ResponseBuilder
from app.database.db import get_db_session
from app.database.user_db import USERDB
from sqlalchemy.future import select
import requests

from app.Models.user import User

router = APIRouter()

@router.get("/user/all")
async def get_all_user(db: AsyncSession = Depends(get_db_session)):
    response = await db.execute(select(USERDB))
    users = response.scalars().all()
    return ResponseBuilder.success(users,status.HTTP_200_OK)

@router.get("/user/{user_id}")
async def get_user(user_id:int, db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(select(USERDB).where(USERDB.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            ResponseBuilder.error("User Not found",status.HTTP_404_NOT_FOUND)
        return ResponseBuilder.success(user,status.HTTP_200_OK)
    except Exception as e:
        print(f"An exception occurred in get_user:{e}")

@router.post("/register")
async def add_user(user:USERDB, db: AsyncSession = Depends(get_db_session)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return ResponseBuilder.success(user, status.HTTP_201_CREATED)

