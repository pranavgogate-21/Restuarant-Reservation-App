from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.database import RestaurantDB
from app.database.db import get_db_session
from app.models.response_builder import ResponseBuilder
from app.models.restaurant import Restaurant, RestaurantUpdate, RestaurantOut
from app.service.auth_service import validate_user
import logging

from app.service.restaurant_service import RestaurantService
from app.service.timeslot_service import get_time_slots_for_restaurant
from app.utils.custom_encoder import ORJSONResponse

router = APIRouter(prefix="/restaurants")

logger = logging.getLogger(__name__)

@router.get("/all", dependencies= [Depends(validate_user)])
async def get_all_restaurants(db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("from get_all_restaurants....")
        response = await db.execute(select(RestaurantDB))
        restaurants = response.scalars().all()
        restaurants = [RestaurantOut.convert_to_api_model(restaurant.model_dump()) for restaurant in restaurants]
        return ORJSONResponse({"data": restaurants}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error("An error occurred in get_all_restaurants")
        raise e

@router.get("/available_slots", dependencies=[Depends(validate_user)])
async def get_available_slots(rest_id:str, booking_date:date, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From get_available_slots....")
        result = await get_time_slots_for_restaurant(rest_id, booking_date, db)
        return ResponseBuilder.success(result, status.HTTP_200_OK)
    except Exception as e:
        logger.error("An error occurred in get_available_slots")
        raise e

@router.get("/{rest_id}", dependencies= [Depends(validate_user)])
async def get_restaurant(rest_id: str, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From get_restaurant....")
        response = await db.execute(select(RestaurantDB).where(RestaurantDB.id == rest_id))
        restaurant = response.scalar_one_or_none()
        if restaurant is None:
            return ResponseBuilder.error("Restaurant not found", status.HTTP_404_NOT_FOUND)
        restaurant = RestaurantOut.convert_to_api_model(restaurant.model_dump())
        return ORJSONResponse({"data": restaurant}, status_code=status.HTTP_200_OK)
    except Exception as e:
        logger.error("An error occurred in get_restaurant")
        raise e

@router.post("", dependencies=[Depends(validate_user)])
async def add_restaurant(restaurant: Restaurant, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From add_restaurant....")
        restaurant = RestaurantDB.convert_to_db_model(restaurant.model_dump())
        db.add(restaurant)
        await db.commit()
        await db.refresh(restaurant)
        restaurant = RestaurantOut.convert_to_api_model(restaurant.model_dump())
        return ORJSONResponse({"data": restaurant}, status.HTTP_201_CREATED)
    except Exception as e:
        logger.error("An error occurred in add_restaurant")
        raise e

@router.patch("/{rest_id}", dependencies=[Depends(validate_user)])
async def update_restaurant(rest_id, restaurant: RestaurantUpdate, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From update_restaurant....")
        res_service = RestaurantService(db)
        result = await res_service.partial_update_restaurant_in_db(rest_id, restaurant)
        result = RestaurantOut.convert_to_api_model(result.model_dump())
        return ORJSONResponse({"data": result}, status.HTTP_200_OK)
    except Exception as e:
        logger.error("An error occurred in update_restaurant")
        raise e

@router.delete("/{rest_id}", dependencies=[Depends(validate_user)])
async def delete_restaurant(rest_id, db: AsyncSession = Depends(get_db_session)):
    try:
        logger.info("From update_restaurant....")
        res_service = RestaurantService(db)
        result = await res_service.delete_restaurant_in_db(rest_id)
        result = RestaurantOut.convert_to_api_model(result.model_dump())
        return ORJSONResponse({"data": result}, status.HTTP_200_OK)
    except Exception as e:
        logger.error("An error occurred in update_restaurant")
        raise e