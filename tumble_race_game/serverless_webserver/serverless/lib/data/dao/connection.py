import boto3
import time
import logging

from typing import Set, List
from socket_config import *
from data.models.connection import Subscription, Connection

log = logging.getLogger(__name__)


class ConnectionDao:
    _CONNECTION_CACHE_DURATION = 5

    def __init__(self):
        self._ddb = boto3.resource('dynamodb', region_name='us-east-1')
        self._conn = self._ddb.Table(DB_CONNECTION_TABLE)
        self._active_connections: List[Connection] = []
        self._active_connections_timestamp = 0

    def get_active_connections(self) -> List[Connection]:
        """
        Caches all active connections from the dynamodb connection table and maintains an in-memory cache
        of open connections.
        """
        if not self._active_connections or \
                time.time() - self._active_connections_timestamp > self._CONNECTION_CACHE_DURATION:

            response = self._conn.scan()
            self._active_connections_timestamp = time.time()
            self._active_connections: List[Connection] = [Connection.from_item(co) for co in
                                                          response.get("Items", [])]
            while 'LastEvaluatedKey' in response:
                response = self._conn.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                next_page = [Connection.from_item(co) for co in response.get("Items", [])]
                self._active_connections = self._active_connections + next_page

        return self._active_connections

    def subscribe(self, connection_id: str, subscriptions: Set[Subscription]) -> bool:
        conn: Connection = self.get_connection(connection_id)
        conn.subscriptions = subscriptions
        return self.put_connection(conn)

    def get_connection(self, connection_id: str) -> Connection:
        result = self._conn.get_item(
            Key={
                DB_CONNECTION_ID_KEY: connection_id
            }
        )
        return Connection.from_item(result.get('Item'))

    def put_connection(self, conn: Connection) -> bool:
        result = self._conn.put_item(Item={
            DB_CONNECTION_ID_KEY: conn.id,
            DB_STAGE_KEY: conn.stage,
            DB_DOMAIN_KEY: conn.domain_name,
            DB_FILTER_EXP_KEY: conn.filter_expr,
            DB_FILTER_FIELD_KEY: conn.filter_field,
            DB_EVENT_TYPE: conn.event_type,
            DB_SUBSCRIPTION_KEY: [x.to_dict() for x in list(conn.subscriptions)],
            TTL_KEY: conn.ttl}
        )
        log.debug(f"Got result: {result} from conn: {conn}")
        return result.get('ResponseMetadata', {}).get('HTTPStatusCode') == 200

    def delete_connection(self, connection_id: str):
        self._conn.delete_item(
            Key={
                DB_CONNECTION_ID_KEY: connection_id
            }
        )
