from handlers.subscription_handler import SubscriptionHandler
from data.dao.connection import ConnectionDao

from utils.logging import LoggingUtils

log = LoggingUtils.configure_logging(__name__)
connection_dao: ConnectionDao = ConnectionDao()

handler = None


def handle(event, context):
    global handler

    if not handler:
        handler = SubscriptionHandler(connection_dao)

    log.info(f"Got event: {event}")
    return handler.subscribe(event, context)
