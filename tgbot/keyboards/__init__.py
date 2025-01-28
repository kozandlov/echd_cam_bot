from enum import Enum

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


class ApproveAction(str, Enum):
    approve = 'Подтвердить'
    decline = 'Начать сначала'


class ApproveCallback(CallbackData, prefix='approve'):
    action: ApproveAction


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


def get_approve_add_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=action.value,
                    callback_data=ApproveCallback(
                        action=action
                    ).pack()
                )
            ] for action in ApproveAction
        ]
    )
