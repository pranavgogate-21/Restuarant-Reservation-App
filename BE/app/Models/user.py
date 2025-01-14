from pydantic import BaseModel, Field, AfterValidator
import re

from typing_extensions import Annotated


def validate_password(password: str):
    print("from validate_password.....")
    if re.search(r'[A-Za-z]', password):
        if re.search(r'\d', password):
            return password
    raise ValueError("Your Password is weak. Tip: Include both numbers and letters")

def validate_phone_number(phone_number: str):
    print("from validate_phone_number......")
    if len(phone_number) != 10 :
        raise ValueError("Phone number must contain exactly 10 digits")
    for char in phone_number:
        if not re.search(r'\d', char):
            raise ValueError("Phone number must contain only digits")
    return phone_number


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
    phone_number: Annotated[str, AfterValidator(validate_phone_number)]

class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = Field(pattern=r'^[^@]+@[^@]+[^@]+\.com$')
    phone_number: Annotated[str, AfterValidator(validate_phone_number)]

class UserPassword(BaseModel):
    old_password: str
    new_password: Annotated[str, Field(min_length=5, pattern=r'^[A-Za-z\d]{5,}$'), AfterValidator(validate_password)]