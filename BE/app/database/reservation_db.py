import uuid
from datetime import date,time
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
    raw_booking_date: str = Field(default={}, sa_column= Column("booking_date"))
    raw_booking_time: str = Field(default={}, sa_column= Column("booking_time"))
    guests:int

    user: Optional["USERDB"] = Relationship(back_populates="reservations")
    restaurant: Optional["RestaurantDB"] = Relationship(back_populates="reservations")

    @property
    def booking_time(self):
        return time.fromisoformat(self.raw_booking_time)

    @booking_time.setter
    def booking_time(self, t:time):
        self.raw_booking_time = t.strftime("%H:%M")

    @property
    def booking_date(self):
        return date.fromisoformat(self.raw_booking_date)

    @booking_date.setter
    def booking_date(self, d: date):
        self.raw_booking_date = d.strftime("%d/%m/%Y")

    @classmethod
    def convert_to_db_model(cls, data:dict):
        instance = cls(**{k: v for k, v in data.items() if k not in ['booking_time', 'booking_date']})
        instance.booking_date = data["booking_date"]
        instance.booking_time = data["booking_time"]


