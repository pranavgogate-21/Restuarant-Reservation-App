from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.response_builder import ResponseBuilder
from app.models.token import TokenOut
from app.auth.jwt_handler import validate_jwt_token, create_access_token, get_payload_data, create_jwt_token
from app.database.token_db import Token
import app.api.login_api as login
from sqlalchemy import and_
from logging import getLogger
logger = getLogger(__name__)


class AuthService:

    def __init__(self, db: AsyncSession):
        logger.info("An instance of Auth Service is created...")
        self.db = db

    async def create_access_token_from_refresh_token(self, token: TokenOut):
        try:
            logger.info("From create_access_token_from_refresh_token")
            token_data = get_payload_data(token.refresh_token)
            user_id = token_data.get("user_id")
            is_valid = await self.check_valid_refresh_and_access_token(token.access_token, token.refresh_token,
                                                                 user_id)
            if not is_valid:
                return False, "Invalid Refresh Token"
            bool_valid, data = validate_jwt_token(token.refresh_token)
            if not bool_valid:
                return False, data
            old_data = get_payload_data(token.access_token)
            access_token = create_access_token(old_data)
            result = await self.db.execute(select(Token).where(Token.user_id == user_id))
            token_obj = result.scalar_one_or_none()
            token_obj.access_token = access_token
            self.db.add(token_obj)
            await self.db.commit()
            await self.db.refresh(token_obj)
            return True, access_token

        except Exception as e:
            logger.error(f"An exception occurred in create_access_token_from_refresh_token:{e}")


    async def check_valid_refresh_and_access_token(self, access_token: str, refresh_token:str, user_id: str ):
        try:
            logger.info("From check_valid_refresh_and_access_token")
            result = await self.db.execute(select(Token).filter(and_(Token.refresh_token == refresh_token,
                                                                        Token.access_token == access_token,
                                                                        Token.user_id == user_id)))
            token_obj = result.scalar_one_or_none()
            if token_obj is None:
                return False
            return True
        except Exception as e:
            logger.error(f"An Exception occurred in check_valid_refresh_and_access_token:{e}")

    async def create_token(self, data:dict):
        try:
            logger.info("From create_token")
            refresh_token, access_token = create_jwt_token(data)
            result = await self.db.execute(select(Token).where(Token.user_id == data.get("user_id")))
            token_obj = result.scalar_one_or_none()
            if token_obj is None:
                token = Token(access_token=access_token, refresh_token=refresh_token, user_id=data.get("user_id"))
                self.db.add(token)
                await self.db.commit()
                await self.db.refresh(token)
                return token
            token_obj.access_token = access_token
            token_obj.refresh_token = refresh_token
            self.db.add(token_obj)
            await self.db.commit()
            await self.db.refresh(token_obj)
            return token_obj

        except Exception as e:
            logger.error(f"An Exception occurred in create_token:{e}")

def validate_user(token : Annotated[str, Depends(login.oauth2_scheme)]):
    logger.info("From get_current_user....")
    is_valid, message = validate_jwt_token(token)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)


