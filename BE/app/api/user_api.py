from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
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
    return users

@router.get("/user/{user_id}")
async def get_user(user_id:int, db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(select(USERDB).where(USERDB.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        print(f"An exception occured in get_user:{e}")

@router.post("/user")
async def add_user(user:USERDB, db: AsyncSession = Depends(get_db_session)):
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

