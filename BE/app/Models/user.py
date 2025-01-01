from pydantic import BaseModel, Field



class User(BaseModel):
    first_name:str
    last_name:str
    email:str
    phone_number:str

    class Config:
        from_attributes = True

class UserIn(BaseModel):
    first_name: str = Field(max_length=15)
    last_name: str = Field(max_length=15)
    email: str = Field(pattern=r'^[^@]+@[^@]+[^@]+\.com$')
    password: str = Field(min_length=5, pattern=r'^[A-Za-z\d]{5,}$')
    phone_number: str = Field(min_length=10, max_length=10, pattern=r'^\d+$')

class UserOut(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone_number: str | None = None

class UserPassword(BaseModel):
    old_password: str
    new_password: str