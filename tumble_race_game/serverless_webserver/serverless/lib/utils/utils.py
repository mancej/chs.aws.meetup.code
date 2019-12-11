import logging

log = logging.getLogger(__name__)


class Utils:

    @staticmethod
    def trace(func):
        def wrapper(*args, **kwargs):
            log.info(f"Entering function: {func.__name__} with args: {args}")
            result = func(*args, **kwargs)
            # log.info(f"Returning result: {result}")
            log.info(f"Exiting function: {func.__name__}")
            return result

        return wrapper
