import json
import logging
from dataclasses import dataclass
from models.messages.socket.type import Type
from models.messages.socket.message import SocketMessage

log = logging.getLogger(__name__)


@dataclass
class ConnectSuccess(SocketMessage):
    connection_id: str
    type: Type = Type.CONNECT_SUCCESS

    def payload(self):
        return {
            "connection_id": self.connection_id
        }

    def msg_type(self):
        return self.type.value
