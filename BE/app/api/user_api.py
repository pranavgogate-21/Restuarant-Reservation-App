from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.Models.response_builder import ResponseBuilder
from app.auth.jwt_handler import validate_jwt_token
from app.database.db import get_db_session
from app.database.user_db import USERDB
from sqlalchemy.future import select

from app.Models.user import User, UserOut, UserPassword
from app.service.user_service import UserService
from app.utils.custom_encoder import ORJSONResponse

router = APIRouter()

@router.get("/user/all")
async def get_all_user(db: AsyncSession = Depends(get_db_session)):
    response = await db.execute(select(USERDB))
    users = response.scalars().all()
    users = [User.from_orm(user) for user in users]
    return ORJSONResponse({"data": users}, status_code=status.HTTP_200_OK)

@router.get("/user/{user_id}")
async def get_user(user_id:str, db: AsyncSession = Depends(get_db_session)):
    try:
        result = await db.execute(select(USERDB).where(USERDB.id == user_id))
        user = result.scalar_one_or_none()
        if user is None:
            ResponseBuilder.error("User Not found",status.HTTP_404_NOT_FOUND)
        user = User.from_orm(user)
        return ORJSONResponse({"data":user}, status_code=status.HTTP_200_OK)

    except Exception as e:
        print(f"An exception occurred in get_user:{e}")

@router.put("/user/{user_id}")
async def update_user(user_id: str, user: UserOut, db: AsyncSession = Depends(get_db_session)):
    try:
        print("From update_user.....")
        user_service = UserService(db)
        is_updated, data = await user_service.update_user_service(user, user_id)
        if not is_updated:
            ResponseBuilder.error(data, status.HTTP_404_NOT_FOUND)
        user = User.from_orm(user)
        return ORJSONResponse({"data": user}, status_code=status.HTTP_200_OK)

    except Exception as e:
        print(f"An exception occurred in update_user:{e}")

@router.patch("/user/{user_id}")
async def update_user_password(user_id: str, password: UserPassword, db:AsyncSession = Depends(get_db_session)):
    try:
        print("From update_user_password....")
        user_service = UserService(db)
        is_updated, data = await user_service.update_password_service(password, user_id)
        if not is_updated:
            ResponseBuilder.error(data, status.HTTP_404_NOT_FOUND)
        return ResponseBuilder.success(data, status.HTTP_200_OK)

    except Exception as e:
        print(f"An exception occurred in update_user_password:{e}")

@router.delete("/user/{user_id}")
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        print("From delete_user.....")
        user_service = UserService(db)
        is_deleted, data = await user_service.delete_user_service(user_id)
        if not is_deleted:
            ResponseBuilder.error(data, status.HTTP_404_NOT_FOUND)
        data = User.from_orm(data)
        return ORJSONResponse({"data": data}, status.HTTP_200_OK)
    except Exception as e:
        print(f"An exception occurred in delete_user:{e}")



