from pydantic import BaseModel, Field, AfterValidator
import re

from typing_extensions import Annotated


def validate_password(password: str):
    if re.search(r'[A-Za-z]', password):
        if re.search(r'\d', password):
            return password
    raise ValueError(f"{password} is weak")


class User(BaseModel):
    first_name:str | None = None
    last_name:str | None = None
    email:str | None = None
    phone_number:str | None = None

    class Config:
        from_attributes = True

class UserIn(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    email: str = Field(pattern=r'^[^@]+@[^@]+[^@]+\.com$')
    password: Annotated[str, Field(min_length=5, pattern=r'^[A-Za-z\d]{5,}$'), AfterValidator(validate_password)]
    phone_number: str = Field(min_length=10, max_length=10, pattern=r'^\d+$')

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = Field(pattern=r'^[^@]+@[^@]+[^@]+\.com$')
    phone_number: str | None = Field(min_length=10, max_length=10, pattern=r'^\d+$')

class UserPassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=5, pattern=r'^[A-Za-z\d]{5,}$'), AfterValidator(validate_password)]