from aiogram.dispatcher.filters import Command


class GetPhotoFromCam(Command):
    def __init__(self):
        super().__init__(['get_photo_from_cam'])


class GetRecordFromCam(Command):
    def __init__(self):
        super().__init__(['record_from_cam'])
