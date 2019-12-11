from enum import Enum


class Type(Enum):
    """
    Represents the various types of SocketMessages that are not Event Messages
    """
    CONNECT_SUCCESS = "ConnectSuccess"
    UNIMPLEMENTED_SOCKET_MESSAGE = "UnimplementedSocketMessage"

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get(cls, value):
        for item in cls:
            if item.value == value:
                return item

        return Type.UNIMPLEMENTED_SOCKET_MESSAGE
