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
            guests = reservation.guests

            query = text("SELECT guests, two_seater, four_seater FROM reservation WHERE restaurant_id = :restaurant_id AND booking_date = :booking_date "
                         "AND booking_time = :booking_time")
            kwargs = {"restaurant_id": reservation.restaurant_id, "booking_date": reservation.booking_date,
                      "booking_time": reservation.booking_time}
            reserve_obj = await self.db.execute(query, kwargs)
            response = reserve_obj.all()
            total_guests = 0
            used_two_seater_count = 0
            used_four_seater_count = 0
            for guest, two_seater, four_seater in response:
                total_guests += guest
                used_two_seater_count += two_seater
                used_four_seater_count += four_seater
            if total_guests + guests > restaurant.capacity :
                return False, "Sorry, Restaurant does not have enough capacity at the given time"

            req_four_seaters = 0
            req_two_seaters = 0
            available_four_seaters = restaurant.four_seater_count - used_four_seater_count
            available_two_seaters = restaurant.two_seater_count - used_two_seater_count
            while guests > 0:
                if guests >= 4 and available_four_seaters:
                    req_four_seaters += 1
                    guests -= 4
                    available_four_seaters -= 1
                elif guests==3 and available_four_seaters:
                    req_four_seaters += 1
                    available_four_seaters -= 1
                    break
                else:
                    req_two_seaters += 1
                    guests -= 2
                    available_two_seaters -= 1

            if req_two_seaters + used_two_seater_count > restaurant.two_seater_count or req_four_seaters + used_four_seater_count > restaurant.four_seater_count:
                return False, "Sorry, Restaurant does not have enough capacity at the given time"

            reservation.two_seater = req_two_seaters
            reservation.four_seater = req_four_seaters

            self.db.add(reservation)
            await self.db.commit()
            await self.db.refresh(reservation)
            return reservation
        except Exception as e:
            logger.error("An error occurred in add_reservation_in_restaurant")
            raise e
            