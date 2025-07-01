from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from logging import getLogger
from app.models.user import UserUpdate, UserPassword
from app.auth.password_config import verify_password, hash_password
from app.database.user_db import USERDB
logger = getLogger(__name__)


class UserService:

     def __init__(self, db:AsyncSession):
         logger.info("UserService instance created...")
         self.db = db

     async def authenticate_user(self, username: str, password: str):
         try:
             logger.info("From authenticate_user ....")
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
             logger.error(f"An exception occurred in authenticate_user:{e}")

     async def update_user_service(self, user: UserUpdate, user_id: str):
         try:
             logger.info("From update_user_service....")
             result = await self.db.execute(select(USERDB).where(USERDB.id == user_id))
             user_obj = result.scalar_one_or_none()
             if user_obj is None:
                 return False, "User Not Found"
             if user.first_name is not None:
                user_obj.first_name = user.first_name
             if user.last_name is not None:
                user_obj.last_name = user.last_name
             if user.email is not None:
                user_obj.email = user.email
             if user.phone_number is not None:
                user_obj.phone_number = user.phone_number
             self.db.add(user_obj)
             await self.db.commit()
             await self.db.refresh(user_obj)
             return True, user_obj
         except Exception as e:
             logger.error(f"An exception occurred in update_user_service:{e}")

     async def update_password_service(self, password: UserPassword, user_id: str):
         try:
             logger.info("From update_password_service....")
             old_password = password.old_password
             new_password = password.new_password
             result = await self.db.execute(select(USERDB).where(USERDB.id == user_id))
             user = result.scalar_one_or_none()
             if not verify_password(old_password, user.password):
                 return False, "Incorrect Password"
             new_password = hash_password(new_password)
             user.password = new_password
             self.db.add(user)
             await self.db.commit()
             await self.db.refresh(user)
             return True, "Password change successful"
         except Exception as e:
             logger.error(f"An exception occurred in update_password_service...:{e}")

     async def delete_user_service(self, user_id: str):
         try:
             logger.info("From delete_user_service....")
             result = await self.db.execute(select(USERDB).where(USERDB.id == user_id))
             user = result.scalar_one_or_none()
             if user is None:
                 return False, "User Not Found"
             await self.db.delete(user)
             await self.db.commit()
             return True, user
         except Exception as e:
             logger.error(f"An exception occurred in delete_user_service:{e}")

