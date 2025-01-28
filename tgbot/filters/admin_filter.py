from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from .. import config


class AdminFilter(BaseFilter):
    is_admin: bool = True

    def __init__(self, is_admin: bool = True):
        self.is_admin = is_admin

    async def __call__(self, obj: Union[Message, CallbackQuery]) -> bool:
        admins_ids = config.tg_bot.admin_ids
        if isinstance(obj, Message):
            return (str(obj.chat.id) in admins_ids) == self.is_admin
        if isinstance(obj, CallbackQuery):
            return (str(obj.message.chat.id) in admins_ids) == self.is_admin
        return False