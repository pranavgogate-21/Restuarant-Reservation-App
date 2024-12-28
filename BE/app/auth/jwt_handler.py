from jose import jwt
from jwt import PyJWKClient
from datetime import datetime, timedelta, timezone
# from app.auth.config import SECRET_KEY, ALGORITHM
SECRET_KEY = "FLDJFASJFLDS209830328LJDLDKJCLDJSLJ2739UJDLFJSLDJF"
ALGORITHM = "HS256"


def create_jwt_token(data:dict, expires_delta: timedelta | None = None):
    token_data = data.copy()
    time_ = datetime.now(timezone.utc)
    expire = time_ + timedelta(minutes=30)
    token_data.update({"iat":time_})
    token_data.update({"exp":expire})
    token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    print(token)

# def validate_jwt_token()

create_jwt_token({"name":"Pranav","user_id":"1djdl23"})