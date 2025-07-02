from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import ReservationDB
from app.database.db import get_db_session
from app.models.reservation import Reservation
from app.service.auth_service import validate_user
import logging

from app.service.reservation_service import ReservationService
from app.utils.custom_encoder import ORJSONResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservations")


@router.post("", dependencies=[Depends(validate_user)])
async def make_reservation(reservation: Reservation, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("An error occurred in make_reservation")
        reservation = ReservationDB.from_orm(reservation)
        res_service = ReservationService(db)
        result = await res_service.add_reservation_in_restaurant(reservation)
        return ORJSONResponse({"data":result}, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error("An error occurred in make_reservation")
        raise e

@router.get("/user/{user_id}", dependencies=[Depends(validate_user)])
async def get_reservation_by_user_id(user_id:str, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("An error occurred in get_reservation_by_user_id")
        result = await db.execute(select(ReservationDB).where(ReservationDB.user_id == user_id))
        result = result.scalars().all()
        return ORJSONResponse({"data":result}, status_code=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error("An error occurred in get_reservation_by_user_id")
        raise e

