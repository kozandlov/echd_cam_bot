from aiogram import Router

from .cameras_management import cameras_router
from .commands import commands_router
from ...filters.admin_filter import AdminFilter

chats_router = Router()

chats_router.message.filter(AdminFilter(is_admin=True))
chats_router.callback_query.filter(AdminFilter(is_admin=True))

chats_router.include_routers(
    commands_router,
    cameras_router
)

__all__ = [
    'chats_router'
]
