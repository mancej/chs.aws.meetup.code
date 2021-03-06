
from typing import Dict
from models.messages.iot.type import Type


class RecordedName:

    def __init__(self, message: Dict):
        super().__init__()
        self._type = Type.RECORDED_NAME
        self.message: Dict = message
        self._socket_format = None

    def type(self) -> Type:
        return Type.RECORDED_NAME

    def msg_type(self) -> str:
        return self.type().value

    def socket_format(self) -> Dict:
        if not self._socket_format:
            self._socket_format = self.message

        return self._socket_format
