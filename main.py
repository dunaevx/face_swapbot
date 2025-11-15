import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config
from db import init_db
from bot.handlers import gif, webapp
from bot.middleware.db import DBMiddleware
from services.face_swap_api import FaceSwapClient
import aiohttp
from asyncpg import create_pool, Pool

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Пул БД
    pool: Pool = await create_pool(
        user=config.db_user,
        password=config.db_pass,
        database=config.db_name,
        host=config.db_host,
        port=config.db_port,
        min_size=1,
        max_size=10
    )
    await init_db(pool)
    
    # Aiohttp сессия
    session = aiohttp.ClientSession()
    api_client = FaceSwapClient(session, config.face_swap_api_url, config.face_swap_api_key)
    
    # Bot
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(DBMiddleware(pool))
    dp.callback_query.middleware(DBMiddleware(pool))
    
    # Роутеры
    dp.include_router(gif.router)
    dp.include_router(webapp.router)
    
    try:
        await dp.start_polling(bot)
    finally:
        await api_client.close()
        await session.close()
        await pool.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())