from typing import Dict, List
from pydantic import BaseModel, model_validator
from datetime import time

class RestaurantBase(BaseModel):
    name: str
    address: str
    image_url: str
    capacity: int
    two_seater_count: int
    four_seater_count: int
    cuisine: str
    working_hours: Dict[str, List[time]]

class Restaurant(RestaurantBase):

    @model_validator(mode="after")
    def validate_capacity_and_seating_count(self):
        if not self.capacity == (2 * self.two_seater_count) + (4 * self.four_seater_count):
            raise ValueError("Total capacity and seat counts do not match!")
        return self

class RestaurantUpdate(RestaurantBase):
    name: str | None =  None
    address: str | None =  None
    image_url: str | None =  None
    capacity: int | None =  None
    two_seater_count: int | None =  None
    four_seater_count: int | None =  None
    cuisine: str | None =  None
    working_hours: Dict[str, List[time]] | None = None

class RestaurantOut(RestaurantBase):
    id: str
    working_hours: Dict[str, List[time]] | None = None

    @staticmethod
    def convert_string_to_time(data: dict[str, List[str]]) -> dict[str, List[time]]:
        return { day: [time.fromisoformat(t) for t in slots] for day, slots in data.items()}

    @classmethod
    def convert_to_api_model(cls, data: dict):
        working_hours = data["raw_working_hours"]
        data = {k:v for k,v in data.items() if k!='raw_working_hours'}
        instance = cls(**data)
        instance.working_hours = cls.convert_string_to_time(working_hours)
        return instance