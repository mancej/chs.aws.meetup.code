import boto3
import logging
from typing import Dict, List
import botocore
from data.models.connection import Connection
from models.messages.socket.message import SocketMessage

log = logging.getLogger(__name__)


class SocketService:

    def __init__(self):
        self._client: Dict = None

    def send_to_connection(self, socket_msg: SocketMessage, connection: Connection) -> None:
        """
        Send a string of data to a client.
        :param socket_msg: message to ship over the socket.
        :param data: Data to send
        :param connection: Populated connection object representing the connection to ship this data to.
        :return:
        """

        if not self._client:
            self._client = boto3.client("apigatewaymanagementapi",
                                        endpoint_url=f"https://{connection.domain_name}/{connection.stage}",
                                        config=botocore.client.Config(max_pool_connections=50))

        try:
            self._client.post_to_connection(ConnectionId=connection.id,
                                        Data=socket_msg.socket_format())
        except self._client.exceptions.GoneException:
            raise ConnectionAbortedError
