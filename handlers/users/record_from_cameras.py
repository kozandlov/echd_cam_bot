import asyncio
import datetime
import os

import cv2
from aiogram.types import Message, CallbackQuery

from data.config import cameras_config
from filters import RecordFromCam
from keyboards.inline import get_addresses_keyboard, cameras_callback_data, get_kabinets_keyboard, get_cameras_keyboard
from loader import dp


@dp.message_handler(RecordFromCam(), is_admin=True)
async def get_photo_from_cam(message: Message):
    await dp.bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await message.answer(
        text='Выберите адрес здания, где установлена камера:',
        reply_markup=get_addresses_keyboard(function='video')
    )


@dp.callback_query_handler(cameras_callback_data.filter(function='video', kabinet='', camera=''), is_admin=True)
async def get_kabinets(call: CallbackQuery, callback_data: dict):
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите кабинет, где установлена камера:',
        reply_markup=get_kabinets_keyboard(callback_data)
    )


@dp.callback_query_handler(cameras_callback_data.filter(function='video', camera=''), is_admin=True)
async def get_camera_names(call: CallbackQuery, callback_data: dict):
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='Выберите камеру, с которой Вы хотите получить изображение:',
        reply_markup=get_cameras_keyboard(callback_data)
    )


@dp.callback_query_handler(cameras_callback_data.filter(function='video'), is_admin=True)
async def get_camera_video(call: CallbackQuery, callback_data: dict):
    url = cameras_config.get(callback_data.get('address')).get(callback_data.get('kabinet')).get(
        callback_data.get('camera')).get('ip-address')
    login = cameras_config.get(callback_data.get('address')).get(callback_data.get('kabinet')).get(
        callback_data.get('camera')).get('login')
    password = cameras_config.get(callback_data.get('address')).get(callback_data.get('kabinet')).get(
        callback_data.get('camera')).get('password')
    await dp.bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text='\n'.join(
            (
                f"Выбрана камера {callback_data.get('camera')}, находящаяся по адресу {callback_data.get('address')} в кабинете {callback_data.get('kabinet')}",
                '',
                'Следующим сообщением вы получите видео с этой камеры'
            )
        ),
        reply_markup=None
    )
    camera_url = f'rtsp://{login}:{password}@{url}:554/cam/realmonitor?channel=1&subtype=0'
    asyncio.get_running_loop().create_task(record_video(camera_url=camera_url, callback_data=callback_data))
    await record_video(camera_url=camera_url, callback_data=callback_data)
    await dp.bot.send_video(
        chat_id=call.message.chat.id,
        video=open(f"{callback_data.get('camera')}.avi", 'rb')
    )
    os.remove(f"{callback_data.get('camera')}.avi")


async def record_video(camera_url: str, callback_data: dict):
    cap = cv2.VideoCapture(camera_url)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    output = cv2.VideoWriter(f"{callback_data.get('camera')}.avi", cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 20,
                             (frame_width, frame_height))
    time_1 = datetime.datetime.now()
    while datetime.datetime.now() - time_1 < datetime.timedelta(minutes=1):
        ret, frame = cap.read()
        if ret == True:
            output.write(frame)
        else:
            print('Stream disconnected')
            break
    output.release()
    cap.release()
