import asyncio
import logging

import betterlogging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage

from tgbot.handlers import handlers_router
from tgbot.services import broadcaster

from tgbot import config


async def on_startup(bot: Bot, admin_ids: list[int] = config.tg_bot.admin_ids):
    await broadcaster.broadcast(bot=bot, users=admin_ids, text="Бот запущен", disable_notification=True)


async def on_shutdown(bot: Bot, admin_ids: list[int] = config.tg_bot.admin_ids):
    await broadcaster.broadcast(bot=bot, users=admin_ids, text="Бот остановлен", disable_notification=True)


def setup_logging():
    log_level = logging.INFO
    betterlogging.basic_colorized_config(level=log_level)

    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting bot")


async def main():
    setup_logging()

    storage = MemoryStorage()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=storage)

    dp.include_routers(*handlers_router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
