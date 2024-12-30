from pydantic import BaseModel

from app.database.user_db import USERDB


class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone_number:str

    class Config:
        from_attributes = True

class UserOut(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None

class UserPassword(BaseModel):
    old_password: str
    new_password: str