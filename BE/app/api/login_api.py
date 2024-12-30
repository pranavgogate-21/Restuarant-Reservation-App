from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.Models.response_builder import ResponseBuilder
from app.auth.jwt_handler import create_jwt_token, validate_jwt_token
from app.auth.password_config import hash_password
from app.database.db import get_db_session
from app.database.user_db import USERDB
from app.Models.LoginRequest import Login
from app.Models.token import TokenOut
from app.service.auth_service import AuthService
from app.service.user_service import UserService
from app.utils.custom_encoder import ORJSONResponse

router = APIRouter()


@router.post("/register")
async def add_user(user: USERDB, db: AsyncSession = Depends(get_db_session)):
    try:
        user.password = hash_password(user.password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return ResponseBuilder.success(user, status.HTTP_201_CREATED)
    except Exception as e:
        print(f"An exception occurred in add_user:{e}")


@router.post("/login")
async def login_user_and_authenticate(login_user: Login, db: AsyncSession = Depends(get_db_session)):
    try:
        username = login_user.username
        password = login_user.password
        user_service = UserService(db)
        auth_service = AuthService(db)
        is_authenticated, data = await user_service.authenticate_user(username, password)
        if not is_authenticated:
            if data == "User not Found":
                return ResponseBuilder.error(data, status.HTTP_404_NOT_FOUND)
            else:
                return ResponseBuilder.error(data, status.HTTP_401_UNAUTHORIZED)
        token = await auth_service.create_token(data)
        token = TokenOut.from_orm(token)
        return ORJSONResponse({"data": token}, status.HTTP_200_OK)
    except Exception as e:
        print(f"An exception occurred in login_user_and_authenticate:{e}")

@router.post("/refresh")
async def refresh_access_token(token: TokenOut, db: AsyncSession = Depends(get_db_session)):
    try:
        print("From refresh_access_token_api.....")
        auth_service = AuthService(db)
        is_created, data = await auth_service.create_access_token_from_refresh_token(token)
        if not is_created:
            return ResponseBuilder.error(data, status.HTTP_401_UNAUTHORIZED)
        return ResponseBuilder.tokens(data, status.HTTP_200_OK)

    except Exception as e:
        print(f"An exception occurred in refresh_access_token:{e}")

