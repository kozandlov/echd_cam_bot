from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data.config import cameras_config

cameras_callback_data = CallbackData('adresses', 'function', 'address', 'kabinet', 'camera')


def get_addresses_keyboard(function: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=address,
                    callback_data=cameras_callback_data.new(
                        function=function,
                        address=address,
                        kabinet='',
                        camera=''
                    )
                )
            ] for address in cameras_config.keys()
        ]
    )


def get_kabinets_keyboard(callback_data: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=kabinet,
                    callback_data=cameras_callback_data.new(
                        function=callback_data.get('function'),
                        address=callback_data.get('address'),
                        kabinet=kabinet,
                        camera=''
                    )
                )
            ] for kabinet in cameras_config.get(callback_data.get('address')).keys()
        ]
    )


def get_cameras_keyboard(callback_data: dict):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=camera,
                    callback_data=cameras_callback_data.new(
                        function=callback_data.get('function'),
                        address=callback_data.get('address'),
                        kabinet=callback_data.get('kabinet'),
                        camera=camera
                    )
                )
            ] for camera in cameras_config.get(callback_data.get('address')).get(callback_data.get('kabinet')).keys()
        ]
    )
