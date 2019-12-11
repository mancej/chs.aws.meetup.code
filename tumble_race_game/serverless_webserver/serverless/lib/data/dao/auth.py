import time
import boto3
import uuid
import logging
from typing import Dict
from socket_config import *

log = logging.getLogger(__name__)


class AuthDao:

    def __init__(self):
        dynamodb = boto3.resource("dynamodb")
        self._auth_table = dynamodb.Table(DB_AUTH_TABLE)

    def token_is_valid(self, token: str) -> bool:
        item = self._auth_table.get_item(
            Key={
                'token_id': token
            }
        )

        if not item.get('Item'):
            log.warning(f"No token found for token: {token}")
            return False
        else:
            return True

    def generate_token(self) -> Dict:
        """
        Generates a valid token and stores it in the token database table. If a user has permissions to invoke
        this function, then they have permissions to generate a token
        """

        ttl = int(time.time() + TOKEN_LIFETIME)
        token = uuid.uuid4()
        self._auth_table.put_item(
            Item={
                DB_TOKEN_ID_KEY: f"{token}",
                TTL_KEY: ttl
            }
        )

        log.debug("Auth token generated successfully.")
        return {DB_TOKEN_ID_KEY: str(token)}
