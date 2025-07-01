import uuid
from datetime import date,time, datetime
from typing import Optional

from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship

from app.database import USERDB
from app.database.restaurant_db import RestaurantDB


class ReservationDB(SQLModel, table=True):
    __tablename__ = "reservation"
    id: str = Field(default_factory= lambda : str(uuid.uuid4()), primary_key=True)
    restaurant_id: str = Field(index=True, foreign_key="restaurant.id", ondelete="CASCADE")
    user_id: str = Field(index=True, foreign_key="userdb.id", ondelete="CASCADE")
    booking_date: date
    booking_time: time
    created_at: datetime = Field(default_factory=datetime.utcnow)
    guests:int

    user: Optional["USERDB"] = Relationship(back_populates="reservations")
    restaurant: Optional["RestaurantDB"] = Relationship(back_populates="reservations")



