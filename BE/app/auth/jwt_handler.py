from jose import jwt, JWTError
from jwt import PyJWKClient
from datetime import datetime, timedelta, timezone
from app.auth.config import SECRET_KEY, ALGORITHM, ISSUER


def create_jwt_token(data:dict, expires_delta: timedelta | None = None):
    token_data = data.copy()
    time_ = datetime.now(timezone.utc)
    expire = time_ + timedelta(minutes=30)
    token_data.update({"iat":time_})
    token_data.update({"exp":expire})
    token_data.update({"iss": ISSUER})
    token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    return token

def validate_jwt_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM, issuer=ISSUER)
        return payload
    except JWTError:
        raise ValueError("Invalid token or token has expired")
