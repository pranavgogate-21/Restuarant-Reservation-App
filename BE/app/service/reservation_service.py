from sqlalchemy import select, and_, text
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio
from app.database import ReservationDB, RestaurantDB
from app.models.reservation import Reservation
import logging
logger = logging.getLogger(__name__)


class ReservationService:
    
    def __init__(self, db:AsyncSession):
        self.db = db
        
    async def add_reservation_in_restaurant(self, reservation: ReservationDB):
        try:
            logger.info("From add_reservation_in_restaurant....")
            result = await self.db.execute(select(RestaurantDB).where(RestaurantDB.id == reservation.restaurant_id))
            restaurant: RestaurantDB = result.scalar_one_or_none()
            if not result:
                return False
            query = text("SELECT guests FROM reservation WHERE restaurant_id = :restaurant_id AND booking_date = :booking_date "
                         "AND booking_time = :booking_time")
            kwargs = {"restaurant_id": reservation.restaurant_id, "booking_date": reservation.booking_date,
                      "booking_time": reservation.booking_time}
            reserve_obj = await self.db.execute(query, kwargs)
            guest_list = reserve_obj.scalars().all()
            total_guests = 0
            for i in guest_list:
                total_guests += i
            if total_guests + reservation.guests > restaurant.capacity :
                return False, "Sorry, Restaurant does not have enough capacity at the given time"
            self.db.add(reservation)
            await self.db.commit()
            await self.db.refresh(reservation)
            return reservation
        except Exception as e:
            logger.error("An error occurred in add_reservation_in_restaurant")
            raise e
            