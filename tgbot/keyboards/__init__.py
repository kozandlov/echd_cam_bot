from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from .. import config
from ..config import Building


class GetBuildingCallBack(CallbackData, prefix='get_building'):
    address: str


class GetBuildingCamerasCallback(CallbackData, prefix='get_cameras'):
    camera_name: str


def get_address_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=building.address,
                    callback_data=GetBuildingCallBack(
                        address=building.address
                    ).pack()
                )
            ] for building in config.buildings
        ]
    )


def get_cameras_for_building_keyboard(building: Building):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=camera.name,
                    callback_data=GetBuildingCamerasCallback(
                        camera_name=camera.name
                    ).pack()
                )
            ] for camera in building.cameras
        ]
    )
