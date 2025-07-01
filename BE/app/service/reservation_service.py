from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ReservationDB
from app.models.reservation import Reservation
import logging
logger = logging.getLogger(__name__)


class ReservationService:
    
    def __init__(self, db:AsyncSession):
        self.db = db
        
    async def add_reservation_in_restaurant(self, reservation: ReservationDB):
        try:
            logger.info("From add_reservation_in_restaurant....")
            self.db.add(reservation)
            await self.db.commit()
            await self.db.refresh(reservation)
            return reservation
        except Exception as e:
            logger.error("An error occurred in add_reservation_in_restaurant")
            raise e
            