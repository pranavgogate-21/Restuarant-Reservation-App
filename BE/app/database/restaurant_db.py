import uuid
from datetime import time
from typing import Dict, List, Optional
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship


class RestaurantDB(SQLModel, table=True):
    __tablename__ = "restaurant"
    id: str = Field(default_factory= lambda : str(uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    address: str
    image_url: str
    capacity: int
    two_seater_count: int
    four_seater_count: int
    cuisine: str
    raw_working_hours: Dict[str, List[str]] = Field(default={}, sa_column=Column("working_hours", JSON))

    reservations: Optional[List["ReservationDB"]] = Relationship(back_populates="restaurant", cascade_delete=True)

    @property
    def working_hours(self) -> Dict[str, List[time]]:
        return {
            day: [time.fromisoformat(t) for t in slots]
            for day, slots in self.raw_working_hours.items()
        }

    @working_hours.setter
    def working_hours(self, value: Dict[str, List[time]]) -> None:
        self.raw_working_hours = {
            day: [t.strftime("%H:%M") for t in slots]
            for day, slots in value.items()
        }

    @classmethod
    def convert_to_db_model(cls, data:dict):
        instance = cls(**{k : v for k,v in data.items() if k!= 'working_hours'})
        instance.working_hours = data["working_hours"]
        return instance

