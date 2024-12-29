from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_

from app.auth.password_config import verify_password
from app.database.user_db import USERDB


class UserService():

     def __init__(self, db:AsyncSession):
         print("UserService instance created...")
         self.db = db

     async def authenticate_user(self, username: str, password: str):
         try:
             print("From authenticate_user ....")
             result = await self.db.execute(select(USERDB).filter(or_(USERDB.email == username, USERDB.phone_number == username)))
             user = result.scalar_one_or_none()
             if user is None:
                 return False,"User not Found"
             if not verify_password(password, user.password):
                 return False, "Incorrect Password"
             data = {}
             data.update({"sub": username})
             data.update({"user_id": user.id})
             data.update({"name": user.first_name})
             return True, data

         except Exception as e:
             print(f"An exception occurred in authenticate_user:{e}")