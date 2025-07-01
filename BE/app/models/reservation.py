import datetime
import uuid

from pydantic import BaseModel

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

class ReservationOut(ReservationUpdate):
    id: str | None = None

    @classmethod
    def convert_to_api_model(cls, data: dict):
        instance = cls(**{k:v for k, v in data.items() if k not in ['booking_time', 'booking_date']})
        instance.booking_date = datetime.date.fromisoformat(data["booking_date"])
        instance.booking_time = datetime.time.fromisoformat(data["booking_time"])
        return instance
