from datetime import date, time, timedelta, datetime
import logging
from collections import defaultdict

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import RestaurantDB, ReservationDB
from app.database.db import get_db_session

logger = logging.getLogger(__name__)

number_to_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

async def get_time_slots_for_restaurant(restaurant_id, booking_date:date, db: AsyncSession):
    try:
        logger.info("From get_time_slots_for_restaurant....")

        response = await db.execute(select(RestaurantDB).where(RestaurantDB.id == restaurant_id))
        restaurant = response.scalar_one_or_none()
        if not restaurant:
            return False
        existing_reservations = await db.execute(
            select(ReservationDB).filter(and_(ReservationDB.restaurant_id == restaurant_id,
                                              ReservationDB.booking_date == booking_date)))
        existing_reservations = existing_reservations.scalars().all()
        guests_per_time_slots = defaultdict(int)
        two_seater_list = defaultdict(int)
        four_seater_list = defaultdict(int)
        for reservation in existing_reservations:
            guests_per_time_slots[reservation.booking_time] += reservation.guests
            two_seater_list[reservation.booking_time] += reservation.two_seater
            four_seater_list[reservation.booking_time] += reservation.four_seater
        working_hours = restaurant.working_hours
        capacity = restaurant.capacity
        total_two_seaters = restaurant.two_seater_count
        total_four_seaters = restaurant.four_seater_count
        day = number_to_days[booking_date.weekday()]
        timings = working_hours[day]
        timings = [datetime.combine(date.today(),timing) for timing in timings]
        start_time = timings[0]
        end_time = timings[1]
        slots = []
        current_time = datetime.now() if booking_date == date.today() else start_time
        while start_time < end_time:
            if start_time >= current_time:
                slots.append(start_time.time())
            start_time += timedelta(minutes=30)
        available_slots = {}
        for slot in slots:
            table_availability = (two_seater_list.get(slot, 0) < total_two_seaters) or (four_seater_list.get(slot, 0) < total_four_seaters)
            slot_capacity = capacity - guests_per_time_slots.get(slot,0) if table_availability else 0
            available_slots[slot.strftime("%H:%M")] = slot_capacity
        return available_slots

    except Exception as e:
        logger.error("An error occurred in get_time_slots_for_restaurant")
        raise e