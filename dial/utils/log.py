# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Loggers used to display information and debug."""

import logging
import sys

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
LOG_FILE = "dial.log"


def get_console_handler():
    """
    Returns a log handler that sends messages through the console.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)

    return console_handler


def get_logger(logger_name):
    """
    Configure and return a Logger by its name.
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(logging.DEBUG)

    logger.addHandler(get_console_handler())

    logger.propagate = False

    return logger


def init_logs():
    """
    Initialize logging system.
    """
    pass
