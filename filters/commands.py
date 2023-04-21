from aiogram.dispatcher.filters import Command


class GetPhotoFromCam(Command):
    def __init__(self):
        super().__init__(['get_photo_from_cam'])
