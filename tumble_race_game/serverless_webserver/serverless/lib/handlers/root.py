import json
import logging
from typing import Union
log = logging.getLogger(__name__)


class RootHandler:

    def _get_body(self, event):
        try:
            return json.loads(event.get("body", ""))
        except:
            log.info("Event body could not be JSON decoded.")
            return {}

    def _get_response(self, status_code, body: Union[str, dict]):
        if not isinstance(body, str):
            body = json.dumps(body)

        return {"statusCode": status_code, "body": body}

    @staticmethod
    def log_response(func):
        def wrapper(*args, **kwargs):
            log.info(f"Function called: {func.__name__} with args: {args}")
            result = func(*args, **kwargs)
            log.info(f"Returned response: {result}")
            return result

        return wrapper
