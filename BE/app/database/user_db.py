from sqlmodel import SQLModel, Field
import uuid

class USERDB(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    email: str = Field(index=True,sa_column_kwargs={"unique": True})
    password: str
    phone_number: str = Field(index=True,sa_column_kwargs={"unique": True})