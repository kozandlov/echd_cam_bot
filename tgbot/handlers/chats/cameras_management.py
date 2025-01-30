from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from magic_filter import F

from ... import config
from ...config import Building, Camera
from ...keyboards import get_cameras_for_building_keyboard, GetBuildingCallBack, get_approve_add_keyboard, \
    ApproveCallback, ApproveAction
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
    building = [building for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите имя новой камеры',
        reply_markup=None
    )
    await state.set_state(AddCameraState.get_camera_name)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building.address,
        }
    )


@cameras_router.callback_query(AddCameraState.get_building, GetBuildingCallBack.filter())
async def get_address_for_new_camera(call: CallbackQuery,
                                     state: FSMContext,
                                     callback_data: GetBuildingCallBack,
                                     bot: Bot):
    building_address = callback_data.address
    building = [building for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите имя новой камеры',
        reply_markup=None
    )
    await state.set_state(AddCameraState.get_camera_name)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building.address,
        }
    )


@cameras_router.message(AddCameraState.get_camera_name)
async def get_login_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    camera_name = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    building_address = (await state.get_data()).get('building_address')
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите IP камеры',
        reply_markup=None
    )
    await state.set_state(AddCameraState.get_ip)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building_address,
            'camera_name': camera_name,
        }
    )


@cameras_router.message(AddCameraState.get_ip)
async def get_ip_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    ip = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    building_address = (await state.get_data()).get('building_address')
    camera_name = (await state.get_data()).get('camera_name')
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите логин для камеры',
        reply_markup=None
    )
    await state.set_state(AddCameraState.get_login)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building_address,
            'camera_name': camera_name,
            'ip': ip,
        }
    )


@cameras_router.message(AddCameraState.get_login)
async def get_login_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    login = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    building_address = (await state.get_data()).get('building_address')
    camera_name = (await state.get_data()).get('camera_name')
    ip = (await state.get_data()).get('ip')
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите пароль для камеры',
        reply_markup=None
    )
    await state.set_state(AddCameraState.get_password)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building_address,
            'camera_name': camera_name,
            'ip': ip,
            'login': login,
        }
    )


@cameras_router.message(AddCameraState.get_password)
async def get_password_for_new_camera(message: Message, bot: Bot, state: FSMContext):
    password = message.text
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    building_address = (await state.get_data()).get('building_address')
    camera_name = (await state.get_data()).get('camera_name')
    ip = (await state.get_data()).get('ip')
    login = (await state.get_data()).get('login')
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='\n'.join(
            [
                'Проверьте правильность заполнения информации',
                '',
                f'Адрес {building_address}',
                f'Имя камеры {camera_name}',
                f'IP камеры {ip}',
                f'Логин {login}',
                f'Пароль {password}'
            ]
        ),
        reply_markup=get_approve_add_keyboard()
    )
    await state.set_state(AddCameraState.finish)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building_address,
            'camera_name': camera_name,
            'ip': ip,
            'login': login,
            'password': password,
        }
    )


@cameras_router.callback_query(AddCameraState.finish, ApproveCallback.filter(F.action == ApproveAction.approve))
async def get_approval_for_new_camera(call: CallbackQuery,
                                      state: FSMContext,
                                      callback_data: ApproveCallback,
                                      bot: Bot):
    building_address = (await state.get_data()).get('building_address')
    building = [building for building in config.buildings if building.address == building_address][0]
    camera = Camera(
        address=building_address,
        name=(await state.get_data()).get('camera_name'),
        ip_address=(await state.get_data()).get('ip'),
        login=(await state.get_data()).get('login'),
        password=(await state.get_data()).get('password'),
    )
    camera.save_to_conf()
    building.cameras.append(
        camera
    )
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Данные успешно сохранены',
        reply_markup=None
    )
    await state.clear()


@cameras_router.callback_query(AddCameraState.finish, ApproveCallback.filter(F.action == ApproveAction.decline))
async def get_decline_for_new_camera(call: CallbackQuery,
                                     state: FSMContext,
                                     callback_data: ApproveCallback,
                                     bot: Bot):
    await bot.delete_message(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    await state.clear()


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
    building = [building for building in config.buildings if building.address == building_address][0]
    edited_message = await bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=(await state.get_data()).get('edited_message'),
        text='Укажите камеру для удаления',
        reply_markup=None if building.cameras is [] else get_cameras_for_building_keyboard(building)
    )
    await state.set_state(DeleteCameraState.get_camera)
    await state.set_data(
        {
            'edited_message': edited_message.message_id,
            'building_address': building.address,
        }
    )
