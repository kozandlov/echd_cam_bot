import os

import cv2
from aiogram.types import Message, CallbackQuery

from data.config import cameras_config
from filters import GetPhotoFromCam
from keyboards.inline import addresses_keyboard, cameras_callback_data, get_kabinets_keyboard, get_cameras_keyboard
from loader import dp


@dp.message_handler(GetPhotoFromCam(), is_admin=True)
async def get_photo_from_cam(message: Message):
    await dp.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer(
        text='Выберите адрес здания, где установлена камера:',
        reply_markup=addresses_keyboard
    )


@dp.callback_query_handler(cameras_callback_data.filter(kab='KabNone'), is_admin=True)
async def get_kabinets(call: CallbackQuery, callback_data: dict):
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите кабинет, где установлена камера:',
        reply_markup=get_kabinets_keyboard(callback_data)
    )


#
@dp.callback_query_handler(cameras_callback_data.filter(cam_name='CamNone'), is_admin=True)
async def get_camera_names(call: CallbackQuery, callback_data: dict):
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите камеру, с которой Вы хотите получить изображение:',
        reply_markup=get_cameras_keyboard(callback_data)
    )


@dp.callback_query_handler(cameras_callback_data.filter(), is_admin=True)
async def get_camera_photo(call: CallbackQuery, callback_data: dict):
    url = cameras_config.get(callback_data.get('address')).get(callback_data.get('kab')).get(
        callback_data.get('cam_name')).get('ip-address')
    login = cameras_config.get(callback_data.get('address')).get(callback_data.get('kab')).get(
        callback_data.get('cam_name')).get('login')
    password = cameras_config.get(callback_data.get('address')).get(callback_data.get('kab')).get(
        callback_data.get('cam_name')).get('password')
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='\n'.join(
            (
                f"Выбрана камера {callback_data.get('cam_name')}, находящаяся по адресу {callback_data.get('address')} в кабинете {callback_data.get('kab')}",
                '',
                'Следующим сообщением вы получите фото с этой камеры'
            )
        ),
        reply_markup=None
    )
    camera_url = f'rtsp://{login}:{password}@{url}:554/cam/realmonitor?channel=1&subtype=0'

    cap = cv2.VideoCapture(camera_url)
    ret, frame = cap.read()
    cv2.imwrite('image.jpg', frame)
    cap.release()
    photo = open('image.jpg', 'rb')
    await dp.bot.send_photo(
        chat_id=call.message.chat.id,
        photo=photo
    )
    photo.close()
    os.remove('image.jpg')
