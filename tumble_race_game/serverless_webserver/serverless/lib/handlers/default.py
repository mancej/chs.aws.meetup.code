import logging
from socket_config import *
from handlers.root import RootHandler

log = logging.getLogger(__name__)


class DefaultHandler(RootHandler):

    def default_message(self, event, context):
        """
        Send back error when unrecognized WebSocket action is received.
        """
        log.info("Unrecognized WebSocket action received.")
        return self._get_response(400, "Unrecognized WebSocket action.")
