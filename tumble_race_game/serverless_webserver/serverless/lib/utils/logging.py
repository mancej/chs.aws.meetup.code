import logging
import sys


class LoggingUtils:

    @staticmethod
    def configure_logging(name: str):
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        stdout_handler = logging.StreamHandler(sys.stdout)
        root_logger.addHandler(stdout_handler)

        log = logging.getLogger(name)
        log.setLevel(logging.INFO)
        return log
