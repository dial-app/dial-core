# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# pylint: disable=global-statement

"""Loggers used to display information and debug."""

import argparse
import logging
import logging.config
import sys
from io import StringIO
from typing import NoReturn

FORMATTER = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S"
)

LOG_FILE = "dial.log"
LOG_STREAM = StringIO()
ROOT_LOGGER = logging.getLogger("")

LOG_LEVEL = logging.INFO


def get_console_handler() -> logging.StreamHandler:
    """
    Returns a log handler that sends its output to a string.
    """
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)

    return console_handler


def get_string_handler() -> logging.StreamHandler:
    """
    Returns a log handler that sends its output to a string.
    """
    string_handler = logging.StreamHandler(LOG_STREAM)
    string_handler.setFormatter(FORMATTER)

    return string_handler


def add_handler_to_root(handler: logging.Handler) -> NoReturn:
    """
    Add a new handler to the logger defined as ROOT
    """
    ROOT_LOGGER.addHandler(handler)


def get_logger(logger_name) -> logging.Logger:
    """
    Configure and return a Logger by its name.
    """
    logger = logging.getLogger(logger_name)

    logger.setLevel(LOG_LEVEL)

    return logger


def init_logs(args: argparse.Namespace) -> NoReturn:
    """
    Initialize logging system.
    """
    global LOG_LEVEL

    # Set specified log level
    try:
        LOG_LEVEL = getattr(logging, args.loglevel.upper())

    except AttributeError:
        raise ValueError("Invalid log level: %s" % args.loglevel)

    # If debug flag, change log level to DEBUG
    if args.debug:
        LOG_LEVEL = logging.DEBUG

    # Configure root logger
    add_handler_to_root(get_console_handler())
    add_handler_to_root(get_string_handler())

    # Configure loggers that could already be initialized (module loggers)
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for logger in loggers:
        logger.setLevel(LOG_LEVEL)

    get_logger(__name__).debug("Logging system initialized.")
