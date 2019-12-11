from handlers.connection import ConnectionHandler
from data.dao.connection import ConnectionDao
from utils.logging import LoggingUtils

log = LoggingUtils.configure_logging(__name__)

handler = None
connection_dao: ConnectionDao = ConnectionDao()


def handle(event, context):
    global handler

    if not handler:
        handler = ConnectionHandler(connection_dao)

    log.info(f"Got event: {event}")
    return handler.handle_connection_event(event, context)
