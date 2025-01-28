from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat


async def set_chat_commands(chat_id: int, bot: Bot):
    await bot.send_message(
        chat_id=chat_id,
        text=' 👇 Команды бота находятся в меню ниже',
    )
    await bot.set_my_commands(
        commands=[
            BotCommand(command='start',
                       description=' 🔄 Сбросить состояние'),
            BotCommand(command='add_camera',
                       description=' ✅Добавить камеру'),
            BotCommand(command='delete_camera',
                       description=' ❌ Удалить камеру'),
            BotCommand(command='get_photo',
                       description=' 📷 Получить фото с камеры'),
        ],
        scope=BotCommandScopeChat(
            chat_id=chat_id
        )
    )
