from handlers.default import DefaultHandler
from utils.logging import LoggingUtils

log = LoggingUtils.configure_logging(__name__)

handler = None


def handle(event, context):
    global handler

    if not handler:
        handler = DefaultHandler()

    log.info(f"Got event: {event}")
    return handler.default_message(event, context)
