from models.messages.iot.type import Type
from models.messages.iot.dash_click import DashClick
from models.messages.iot.nes_click import NESClick
from models.messages.iot.photo_upload import PhotoUpload
from models.messages.iot.photo_cropped import PhotoCropped
from models.messages.iot.transcribe_event import TranscribeEvent
from typing import Dict
import logging

log = logging.getLogger(__name__)


class MessageFactory:

    @staticmethod
    def instance(type: Type, message: Dict):
        if type == Type.DASH_CLICK:
            return DashClick(message)
        elif type == Type.NES_CLICK:
            return NESClick(message)
        elif type == Type.PHOTO_UPLOAD:
            return PhotoUpload(message)
        elif type == Type.PHOTO_CROPPED:
            return PhotoCropped(message)
        elif type == Type.TRANSCRIBE_EVENT:
            return TranscribeEvent(message)
        else:  # AKA DefaultType
            raise NotImplementedError(f"Provided type of: {type} is not supported.")

