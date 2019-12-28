# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Loggers used to display information and debug."""

import logging
import sys
from io import StringIO

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S"
)
LOG_FILE = "dial.log"
LOG_STREAM = StringIO()
ROOT_HANDLER = logging.getLogger("")


def get_console_handler():
    """
    Returns a log handler that sends its output to a string.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)

    return console_handler


def get_string_handler():
    """
    Returns a log handler that sends its output to a string.
    """
    string_handler = logging.StreamHandler(LOG_STREAM)
    string_handler.setFormatter(FORMATTER)

    return string_handler


def add_handler_to_root(handler: logging.Handler):
    """
    Add a new handler to the logger defined as ROOT
    """
    ROOT_HANDLER.addHandler(handler)


def get_logger(logger_name):
    """
    Configure and return a Logger by its name.
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    return logger


def init_logs():
    """
    Initialize logging system.
    """

    # Configure root logger
    add_handler_to_root(get_console_handler())
    add_handler_to_root(get_string_handler())

    # logging.getLogger("").setLevel(logging.DEBUG)

    get_logger(__name__).debug("Logging system initialized")
