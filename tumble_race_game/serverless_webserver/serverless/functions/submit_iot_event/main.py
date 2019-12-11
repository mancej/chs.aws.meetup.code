from handlers.iot import IotHandler
from utils.logging import LoggingUtils

log = LoggingUtils.configure_logging(__name__)

handler = None


def handle(event, context):
    global handler

    if not handler:
        handler = IotHandler()

    log.info(f"Got event: {event}")
    return handler.submit_iot_event(event, context)
