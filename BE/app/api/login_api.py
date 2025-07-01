from typing import Annotated
import logging
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.response_builder import ResponseBuilder
from app.models.user import User, UserIn
from app.auth.password_config import hash_password
from app.database.db import get_db_session
from app.database.user_db import USERDB
from app.models.token import TokenOut
import app.service.auth_service as authservice
from app.service.user_service import UserService
from app.utils.custom_encoder import ORJSONResponse
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

@router.post("/register")
async def add_user(user_in: UserIn, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From add_user api.....")
        user = USERDB.model_validate(user_in)
        user.password = hash_password(user.password)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        user = User.from_orm(user)
        return ORJSONResponse({"data": user}, status.HTTP_201_CREATED)
    except Exception as e:
        logger.error(f"An exception occurred in add_user:{e}")


@router.post("/login")
async def login_user_and_authenticate(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From login_user_and_authenticate....")
        username = form_data.username
        password = form_data.password
        user_service = UserService(db)
        auth_service = authservice.AuthService(db)
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
        logger.error(f"An exception occurred in login_user_and_authenticate:{e}")

@router.post("/refresh")
async def refresh_access_token(token: TokenOut, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From refresh_access_token_api.....")
        auth_service = authservice.AuthService(db)
        is_created, data = await auth_service.create_access_token_from_refresh_token(token)
        if not is_created:
            return ResponseBuilder.error(data, status.HTTP_401_UNAUTHORIZED)
        return ResponseBuilder.tokens(data, status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"An exception occurred in refresh_access_token:{e}")

