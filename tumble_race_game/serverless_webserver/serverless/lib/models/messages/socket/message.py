from abc import ABC, abstractmethod
import logging
import json

log = logging.getLogger(__name__)


class SocketMessage(ABC):
    MSG_TYPE_KEY = "message_type"
    PAYLOAD_KEY = "payload"

    @abstractmethod
    def msg_type(self) -> str:
        pass

    @abstractmethod
    def payload(self) -> str:
        pass

    def socket_format(self) -> bytes:
        return json.dumps({
            self.MSG_TYPE_KEY: self.msg_type(),
            self.PAYLOAD_KEY: self.payload(),
        }).encode('utf-8')
