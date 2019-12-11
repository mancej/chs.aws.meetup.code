import json
import logging
from dataclasses import dataclass
from typing import List, Dict, Any
from models.messages.socket.message import SocketMessage

log = logging.getLogger(__name__)


@dataclass
class Event(SocketMessage):
    """
    Represents a generic event in SocketMessage format that may be shipped over any websocket.
    """
    message: Any

    def __init__(self, message: Any, desired_fields: List[str] = None):
        self.message = message
        self.desired_fields: List[str] = desired_fields

    def get_formatted_message(self) -> str:
        if not self.desired_fields:
            return json.dumps(self.message.socket_format())

        msg_dict: Dict = self.message.socket_format()
        results: Dict = {}

        for desired_field in self.desired_fields:
            sub_fields: List = desired_field.split(".")

            first = True
            last_item = {}
            for field in sub_fields:
                last_item = msg_dict.get(field, {}) if first else last_item.get(field, {})
                first = False

            results[desired_field] = last_item

        return json.dumps(results)

    def payload(self) -> str:
        return self.get_formatted_message()

    def msg_type(self) -> str:
        return self.message.msg_type()

    def __str__(self) -> str:
        return f"{self.__dict__}"
