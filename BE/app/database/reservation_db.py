import uuid
from datetime import date,time, datetime
from typing import Optional
import enum
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship, Enum

from app.database import USERDB
from app.database.restaurant_db import RestaurantDB

class BookingStatus(str, enum.Enum):
    active = "ACTIVE"
    cancelled = "CANCELLED"
    completed = "COMPLETED"

class ReservationDB(SQLModel, table=True):
    __tablename__ = "reservation"
    id: str = Field(default_factory= lambda : str(uuid.uuid4()), primary_key=True)
    restaurant_id: str = Field(index=True, foreign_key="restaurant.id", ondelete="CASCADE")
    user_id: str = Field(index=True, foreign_key="userdb.id", ondelete="CASCADE")
    booking_date: date = Field(index=True)
    booking_time: time = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    two_seater: int | None = None
    four_seater: int | None = None
    status: BookingStatus = Field(sa_column=Column(Enum(BookingStatus)), default=BookingStatus.active)
    guests:int

    user: Optional["USERDB"] = Relationship(back_populates="reservations")
    restaurant: Optional["RestaurantDB"] = Relationship(back_populates="reservations")






