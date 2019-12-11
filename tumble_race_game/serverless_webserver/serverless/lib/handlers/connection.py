import time
import logging
from socket_config import *
from handlers.root import RootHandler
from data.models.connection import Connection
from typing import Any, Dict

log = logging.getLogger(__name__)


class ConnectionHandler(RootHandler):

    def __init__(self, connection_dao: Any):
        self._conn = connection_dao

    @RootHandler.log_response
    def __connect(self, connection: Connection) -> Dict[str, str]:
        self._conn.put_connection(connection)
        log.debug(f"Got connection: {self._conn.get_connection(connection.id)}")

        return self._get_response(200, {'connection_id': connection.id})

    @RootHandler.log_response
    def __disconnect(self, connection: Connection) -> Dict[str, str]:
        self._conn.delete_connection(connection.id)
        return self._get_response(200, "Disconnect successful.")

    def __get_connection(self, connection_id: str) -> Connection:
        return self._conn.get_connection(connection_id)

    def handle_connection_event(self, event, context):
        """
        Handles connecting and disconnecting for the Websocket.
        Disconnect removes the connection_id from the database.
        Connect inserts the connection_id to the database.
        """

        connection_id = event["requestContext"].get("connectionId")
        action_type = event["requestContext"].get("eventType")

        if not connection_id:
            log.error("Failed: connectionId value not set.")
            return self._get_response(500, "connectionId value not set.")

        if action_type == Constants.Action.CONNECT:
            log.info(f"Connect requested (CID: {connection_id}")
            conn = self.__build_connection(event)
            return self.__connect(conn)

        elif action_type == Constants.Action.DISCONNECT:
            log.info(f"Disconnect requested (CID: {connection_id}")
            conn = self.__get_connection(connection_id)
            return self.__disconnect(conn)

        else:
            log.error("Connection manager received unrecognized eventType '{}'".format(action_type))
            return self._get_response(500, "Unrecognized eventType.")

    def __build_connection(self, event: Dict) -> Connection:
        connection_id = event["requestContext"].get("connectionId")
        stage = event["requestContext"].get("stage")
        domain_name = event["requestContext"].get("domainName")
        filter_field = event.get("queryStringParameters", {}).get(URL_FILTER_FIELD_KEY, None)
        filter_expression = event.get("queryStringParameters", {}).get(URL_FILTER_EXP_KEY, None)
        event_type = event.get("queryStringParameters", {}).get(URL_EVENT_TYPE_KEY, None)

        return Connection(
            id=connection_id,
            stage=stage,
            domain_name=domain_name,
            filter_field=filter_field,
            filter_expr=filter_expression,
            event_type=event_type,
            ttl=int(time.time()) + TOKEN_LIFETIME,
            subscriptions=set()
        )
