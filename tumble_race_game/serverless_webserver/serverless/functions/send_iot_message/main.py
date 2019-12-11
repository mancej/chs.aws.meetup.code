from handlers.iot import IotHandler
from utils.logging import LoggingUtils

log = LoggingUtils.configure_logging(__name__)

handler = None


def handle(event, context):
    global handler

    if not handler:
        handler = IotHandler()

    return handler.send_message(event, context)
