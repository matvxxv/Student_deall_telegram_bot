import asyncio
import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine
from aiogram import Bot, Dispatcher

from database.base import get_session_maker, init_db_model
from database.models import User, Order

from create_bot import Config, load_config
from updates_worker import get_handled_updates_list

from middleware.register_check import RegisterCheck

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    config: Config = load_config()
    engine = create_async_engine(
        f'postgresql+asyncpg://{config.db.user}:{config.db.password}@{config.db.host}/{config.db.db_name}',
        future=True,
        echo=True
    )

    await init_db_model(engine, User.metadata)
    await init_db_model(engine, Order.metadata)

    async_sessionmaker = await get_session_maker(engine)
    bot = Bot(config.bot.token, parse_mode="HTML")
    bot['db'] = async_sessionmaker
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(RegisterCheck())
    from handlers import client, create_order
    create_order.register_order_handlers(dp)
    client.register_handlers_client(dp)

    try:
        await dp.start_polling(bot, allowed_updates=get_handled_updates_list(dp))
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")
