from pydantic import BaseModel

from app.database.user_db import USERDB


class User(BaseModel):
    id:str
    first_name:str
    last_name:str
    email:str
    phone_number:str

    class Config:
        from_attributes = True
