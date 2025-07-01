from jose import jwt, JWTError
from jwt import PyJWKClient
import time
from datetime import datetime, timedelta, timezone
from app.auth.config import SECRET_KEY, ALGORITHM, ISSUER
from logging import getLogger
logger = getLogger(__name__)

def create_jwt_token(data:dict, expires_delta: timedelta | None = None):
    token_data = data.copy()
    refresh_token_data = {}
    time_ = datetime.now(timezone.utc)
    expire = time_ + timedelta(minutes=30)
    refresh_expire = time_ + timedelta(days=1)
    refresh_token_data["user_id"] = data.get("user_id","")
    refresh_token_data.update({"iat": time_})
    refresh_token_data.update({"exp": refresh_expire})
    refresh_token_data.update({"iss": ISSUER})
    refresh_token = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)
    token_data.update({"iat":time_})
    token_data.update({"exp":expire})
    token_data.update({"iss": ISSUER})
    token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    return refresh_token, token

def create_access_token(data: dict):
    token_data = data.copy()
    time_ = datetime.now(timezone.utc)
    expire = time_ + timedelta(minutes=30)
    token_data.update({"iat": time_})
    token_data.update({"exp": expire})
    token_data.update({"iss": ISSUER})
    token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    return token

def validate_jwt_token(token: str):
    try:
        data = jwt.get_unverified_claims(token)
        if data["iss"] != ISSUER:
            logger.info("Invalid Token Issuer mismatch")
            return False, "Invalid Token"
        if int(datetime.now(timezone.utc).timestamp()) > data["exp"]:
            logger.info("Expired token")
            return False, "Token expired"
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM, issuer=ISSUER)
        return True, payload
    except JWTError:
        raise ValueError("Invalid token or token has expired")

def get_payload_data(token: str):
    try:
        return jwt.get_unverified_claims(token)
    except Exception as e:
        logger.error(f"An error occurred in get_payload_data:{e}")
