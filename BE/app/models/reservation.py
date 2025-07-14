import datetime
import uuid
import enum
from pydantic import BaseModel
from app.database.reservation_db import BookingStatus

class Reservation(BaseModel):
    booking_date: datetime.date
    booking_time: datetime.time
    restaurant_id: str
    user_id: str
    guests: int


class ReservationUpdate(Reservation):
    booking_date: datetime.date | None = None
    booking_time: datetime.time| None = None
    restaurant_id: str | None = None
    user_id: str | None = None
    guests: int | None = None

class ReservationOut(Reservation):
    id: str | None = None
    status: BookingStatus

    class Config:
        from_attributes = True
