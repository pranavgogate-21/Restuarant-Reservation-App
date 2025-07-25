from fastapi import FastAPI
from app.database.db import init_db
import uvicorn
import logging
from app.logger.logger import setup_logging
from app.api import user_api, login_api, restaurant_api, reserve_api

app = FastAPI()
setup_logging()
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def on_startup():
    logger.info("Starting the Fastapi application.....")
    await init_db()
app.include_router(user_api.router, tags="user")
app.include_router(login_api.router, tags="auth")
app.include_router(restaurant_api.router)
app.include_router(reserve_api.router)

if __name__ == "__main__" :
    uvicorn.run(app,host="0.0.0.0",port=8000)
