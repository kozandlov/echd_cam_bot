from aiogram import Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from .data import set_chat_commands
from ... import config
from ...keyboards import get_address_keyboard
from ...states import AddCameraState, DeleteCameraState, GetPhotoState

commands_router = Router()


@commands_router.message(CommandStart())
async def start_command(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    if (await state.get_data()).get('edited_message'):
        await bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await state.get_data()).get('edited_message')
        )
    await state.clear()
    await set_chat_commands(
        chat_id=message.chat.id,
        bot=bot
    )


@commands_router.message(Command('add_camera'))
async def add_camera(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    edited_message = await message.answer(
        text='Введите адрес здания или выберите из существующих',
        reply_markup=None if config.buildings is [] else get_address_keyboard()
    )
    await state.set_state(AddCameraState.get_building)
    await state.set_data(
        {
            'edited_message': edited_message.message_id
        }
    )


@commands_router.message(Command('delete_camera'))
async def delete_camera(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    if len(config.buildings) == 0:
        await message.answer(
            text='Я еще не знаю ни об одной камере',
            reply_markup=None
        )
        return
    edited_message = await message.answer(
        text='Введите адрес здания или выберите из существующих',
        reply_markup=None if config.buildings is [] else get_address_keyboard()
    )
    await state.set_state(DeleteCameraState.get_building)
    await state.set_data(
        {
            'edited_message': edited_message.message_id
        }
    )


@commands_router.message(Command('get_photo'))
async def get_photo(message: Message, bot: Bot, state: FSMContext):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    edited_message = await message.answer(
        text='Введите адрес здания или выберите из существующих',
        reply_markup=None if config.buildings is [] else get_address_keyboard()
    )
    await state.set_state(GetPhotoState.get_building)
    await state.set_data(
        {
            'edited_message': edited_message.message_id
        }
    )
