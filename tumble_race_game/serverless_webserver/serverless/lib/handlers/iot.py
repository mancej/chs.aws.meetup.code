import base64
import boto3
import json
import logging
import time
from typing import List, Dict
from handlers.root import RootHandler
from data.dao.connection import ConnectionDao
from svcs.socket import SocketService
from concurrent.futures import ThreadPoolExecutor
from data.models.connection import Connection
from socket_config import *
from models.messages.iot.type import Type
from models.messages.iot.factory import MessageFactory
from models.messages.socket.event import Event as SocketEvent
from botocore.client import ClientError

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class IotHandler(RootHandler):

    def __init__(self):
        self._conn: ConnectionDao = ConnectionDao()
        self._socket: SocketService = SocketService()

    def _forward_message(self, message: Dict) -> int:
        msg_type_str = message.get(MESSAGE_TYPE_KEY, None)
        msg_type: Type = Type(msg_type_str) if Type.has_value(msg_type_str) else Type("UnimplementedMessage")
        sent_count = 0

        try:
            message = MessageFactory.instance(msg_type, message[MESSAGE_KEY])
        except NotImplementedError:
            log.warning(f"Message of type: {msg_type_str} is not a valid message type.")
            return 0
        else:
            active_connections: List[Connection] = self._conn.get_active_connections()

            for connection in active_connections:
                if not connection.is_gone:
                    for sub in connection.subscriptions:
                        if sub.event_type == msg_type_str:
                            try:
                                self._socket.send_to_connection(SocketEvent(message, sub.desired_fields),
                                                                connection)
                                sent_count += 1
                                break
                            except ConnectionAbortedError as e:
                                log.warning(f"Marking connection as gone: {connection}.")
                                connection.is_gone = True

        return sent_count

    def send_message(self, event, context):
        records = event['Records']
        log.info(f"Processing records: {records}")
        count = 0

        for record in records:
            event_msg = base64.b64decode(record['kinesis']['data']).decode()
            count = count + self._forward_message(json.loads(event_msg))

        log.debug(f"{count} messages sent to viewers.")
        return self._get_response(200, "Messages processed")

    def submit_iot_event(self, event, context):
        log.info(f"Got event: {event}")
        event_body = json.loads(event.get("body", {}))
        log.info(f"Got body: {event_body}")
        self._forward_message(event_body.get('event'))
