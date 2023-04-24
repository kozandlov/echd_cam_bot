from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import cameras_config

cameras_callback_data = CallbackData('cam_callbacks', 'function', 'address', 'kab', 'cam_name')


def get_addresses_keyboard(function: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=address,
                    callback_data=cameras_callback_data.new(
                        function=function,
                        address=address,
                        kab='KabNone',
                        cam_name='None'
                    )
                )
            ] for address in cameras_config.keys()
        ]
    )


#
def get_kabinets_keyboard(callback_data: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=kabinet,
                    callback_data=cameras_callback_data.new(
                        function=callback_data.get('function'),
                        address=callback_data.get('address'),
                        kab=kabinet,
                        cam_name='CamNone'
                    )
                )
            ] for kabinet in cameras_config.get(callback_data.get('address')).keys()
        ]
    )


#
def get_cameras_keyboard(callback_data: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=camera,
                    callback_data=cameras_callback_data.new(
                        function=callback_data.get('function'),
                        address=callback_data.get('address'),
                        kab=callback_data.get('kab'),
                        cam_name=camera
                    )
                )
            ] for camera in cameras_config.get(callback_data.get('address')).get(callback_data.get('kab')).keys()
        ]
    )
