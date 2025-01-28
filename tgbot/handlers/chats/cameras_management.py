from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from ... import config
from ...config import Building
from ...keyboards import get_cameras_for_building_keyboard, GetBuildingCallBack
from ...states import AddCameraState, DeleteCameraState

cameras_router = Router()


@cameras_router.message(AddCameraState.get_building)
async def get_address_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    building_address = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    if building_address not in [building.address for building in config.buildings]:
        config.buildings.append(Building(address=building_address, cameras=[]))
    building = [building.address for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите имя новой камеры'
    )
    await state.set_state(AddCameraState.get_camera_name)
    await state.set_data(
        {
            'edited_message': edited_message,
            'building_address': building.address,
        }
    )


@cameras_router.callback_query(AddCameraState.get_building)
async def get_address_for_new_camera(call: CallbackQuery,
                                     state: FSMContext,
                                     callback_data: GetBuildingCallBack,
                                     bot: Bot):
    building_address = callback_data.address
    building = [building.address for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите имя новой камеры'
    )
    await state.set_state(AddCameraState.get_camera_name)
    await state.set_data(
        {
            'edited_message': edited_message,
            'building_address': building.address,
        }
    )


@cameras_router.message(DeleteCameraState.get_building)
async def get_address_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    building_address = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    if building_address not in [building.address for building in config.buildings]:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=(await state.get_data()).get('edited_message'),
            text='Вы указали несуществующий адрес'
        )
        await state.clear()
        return
    building = [building.address for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите камеру для удаления',
        reply_markup=None if building.cameras is [] else get_cameras_for_building_keyboard(building)
    )
    await state.set_state(DeleteCameraState.get_camera)
    await state.set_data(
        {
            'edited_message': edited_message,
            'building_address': building.address,
        }
    )
