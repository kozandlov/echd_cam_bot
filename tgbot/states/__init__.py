from aiogram.fsm.state import StatesGroup, State


class AddCameraState(StatesGroup):
    get_building = State()
    get_camera_name = State()
    get_ip = State()
    get_login = State()
    get_password = State()
    finish = State()


class DeleteCameraState(StatesGroup):
    get_building = State()
    get_camera = State()
    finish = State()


class GetPhotoState(StatesGroup):
    get_building = State()
    get_camera = State()
    finish = State()
