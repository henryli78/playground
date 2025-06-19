import logging

# Configure logging with timestamp (no comma between seconds and milliseconds)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d:%(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Log:
    @staticmethod
    def info(msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        logging.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        logging.error(msg, *args, **kwargs)

    @staticmethod
    def debug(msg, *args, **kwargs):
        logging.debug(msg, *args, **kwargs)

    @staticmethod
    def critical(msg, *args, **kwargs):
        logging.critical(msg, *args, **kwargs)

    @staticmethod
    def exception(msg, *args, **kwargs):
        """Logs an error message along with the exception traceback."""
        logging.exception(msg, *args, **kwargs)
