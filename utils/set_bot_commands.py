from aiogram import types, Dispatcher
from aiogram.types import BotCommandScopeChat, Message


async def set_chat_commands(dp: Dispatcher, message: Message):
    await dp.bot.set_my_commands(commands=[
        types.BotCommand("start", "Запустить бота"),
        types.BotCommand("help", "Вывести справку"),
        types.BotCommand("get_photo_from_cam", "Получить фото с камеры"),
        types.BotCommand('record_from_cam', 'Записать видео с камеры')
    ],
        scope=BotCommandScopeChat(chat_id=message.chat.id)
    )
