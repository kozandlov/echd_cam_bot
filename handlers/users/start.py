from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp
from utils.set_bot_commands import set_chat_commands


@dp.message_handler(CommandStart(), is_admin=True)
async def bot_start(message: types.Message):
    await set_chat_commands(dp=dp, message=message)
    await message.answer('\n'.join(
        (
            f"Привет, {message.from_user.full_name}!",
            "Все функции бота представлены в меню ниже"
        )
    )
    )


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer('\n'.join(
        (
            f"Привет, {message.from_user.full_name}!",
            "Вы не являетесь администратором.",
            "Для получения доступа попросите IT-куратора предоставить вам доступ."
        )
    )
    )
