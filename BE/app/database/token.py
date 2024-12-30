from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey

from sqlmodel import SQLModel, Field, Relationship



class Token(SQLModel,table=True):
    id: int | None = Field(default=None, primary_key=True)
    access_token: str = Field(index=True)
    refresh_token: str = Field(index=True)
    user_id: str = Field(...,foreign_key="userdb.id", unique=True, ondelete="CASCADE")

    user: Optional["USERDB"] = Relationship(back_populates="tokens")

