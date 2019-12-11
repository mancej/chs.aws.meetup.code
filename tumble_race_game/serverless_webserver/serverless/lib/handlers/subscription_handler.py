import logging
import json
from typing import Set, List
from data.models.connection import Subscription
from handlers.root import RootHandler
from typing import Any

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class SubscriptionHandler(RootHandler):

    def __init__(self, connection_dao: Any):
        self._connection = connection_dao

    def subscribe(self, event, context):
        log.debug(f"Got subscription event: {event} with context: {context}")
        connection_id = event["requestContext"].get("connectionId")
        body = json.loads(event.get("body", "{}"))
        sub_list: List = body.get("subscriptions", {})

        subscriptions: Set[Subscription] = set([Subscription.from_value(item) for item in sub_list])

        if self._connection.subscribe(connection_id, subscriptions):
            return self._get_response(200, "Subscription success.")
        else:
            return self._get_response(500, "Subscription failure.")

