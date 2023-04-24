import typing

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if isinstance(obj, types.Message):
            if not self.is_admin:
                return False
            return str(obj.chat.id) in config.ADMINS
        if isinstance(obj, types.CallbackQuery):
            if not self.is_admin:
                return False
            return str(obj.message.chat.id) in config.ADMINS
