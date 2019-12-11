from enum import Enum
import logging

log = logging.getLogger(__name__)


class Type(Enum):
    # Generic
    UNIMPLEMENTED_MESSAGE = "UnimplementedMessage"

    # IOT Message
    DASH_CLICK = "DashClick"
    NES_CLICK = "NESClick"
    PHOTO_UPLOAD = "PhotoUpload"
    PHOTO_CROPPED = "PhotoCropped"
    RECORDED_NAME = "RecordedName"
    TRANSCRIBE_EVENT = "TranscribeEvent"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get(cls, value):
        for item in cls:
            if item.value == value:
                return item

        return Type.UNIMPLEMENTED_MESSAGE
