import logging
from fastapi import HTTPException, status
from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import RestaurantDB
from app.models.restaurant import RestaurantUpdate, Restaurant, RestaurantOut

logger = logging.getLogger(__name__)

class RestaurantService:

    def __init__(self, db: AsyncSession):
        logger.info("An instance of RestaurantService has been created")
        self.db = db

    async def partial_update_restaurant_in_db(self, rest_id: str, update_item: RestaurantUpdate):
        logger.info("From update_restaurant_in_db....")
        result = await self.db.execute(select(RestaurantDB).where(RestaurantDB.id == rest_id))
        restaurant = result.scalar_one_or_none()
        if restaurant is None:
            raise HTTPException(detail="Restaurant Not Found", status_code=status.HTTP_404_NOT_FOUND)
        try:
            restaurant = RestaurantOut.convert_to_api_model(restaurant.model_dump()).model_dump()
            update_item = update_item.model_dump()
            for key, value in restaurant.items():
                if update_item.get(key, None) is not None:
                    restaurant[key] = update_item[key]
            new_item = RestaurantDB.convert_to_db_model(restaurant)
            await self.db.execute(update(RestaurantDB).where(RestaurantDB.id == new_item.id).values(new_item.model_dump()))
            await self.db.commit()
            result = await self.db.execute(select(RestaurantDB).where(RestaurantDB.id == rest_id))
            result = result.scalar_one_or_none()
            return result
        except Exception as e:
            logger.error("An error occurred in update_restaurant_in_db")
            raise e

    async def delete_restaurant_in_db(self, rest_id):
        logger.info("From delete_restaurant_in_db....")
        result = await self.db.execute(select(RestaurantDB).where(RestaurantDB.id == rest_id))
        restaurant = result.scalar_one_or_none()
        if restaurant is None:
            raise HTTPException(detail="Restaurant Not Found", status_code=status.HTTP_404_NOT_FOUND)
        try:
            await self.db.delete(restaurant)
            await self.db.commit()
        except Exception as e:
            logger.error("An error occurred in delete_restaurant_in_db")
            raise e