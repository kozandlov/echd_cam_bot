from aiogram import Dispatcher

from loader import dp
from .AdminFilter import AdminFilter
from .commands import GetPhotoFromCam

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    pass

__all__ = [GetPhotoFromCam]
