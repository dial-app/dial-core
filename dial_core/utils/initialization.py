# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
"""
Functions to check that python versions, libraries... used by the program are correct.
"""


import argparse
import sys
from typing import List

from dial_core.utils import log
from dial_core.utils.log import DEBUG, log_on_end

LOGGER = log.get_logger(__name__)


def initialize(args: "argparse.Namespace"):
    """Performs all the necessary steps before running the application. This checks
    python version, installed modules, initialize logging system...

    Raises:
        ImportError: If couldn't import a necessary module.
        SystemError: If the Python version isn't compatible.
    """
    # Init logs system
    log.init_logs(args)

    # Check correct python and module versions
    check_python_version()


def parse_args(sys_args: List) -> "argparse.Namespace":
    """Parses the system arguments (sys.arg), returning the app configuration.

    Args:
        sys_args: List of arguments to parse.

    Returns:
        A Namespace object (simillar to a dict) with the parsed configuration
    """
    return get_arg_parser().parse_args(sys_args)


def get_arg_parser() -> "argparse.ArgumentParser":
    """
    Returns:
        An argument parser for this application.
    """
    parser = argparse.ArgumentParser(prog="dial")

    parser.add_argument(
        "-d", "--debug", help="Show debug messages", action="store_true"
    )

    parser.add_argument(
        "-l",
        "--loglevel",
        dest="loglevel",
        help="Set logging level",
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
    )

    return parser


@log_on_end(DEBUG, f"Python Version: {sys.version}", logger=LOGGER)
def check_python_version():
    """
    Check if Python version installed is correct.

    Raises:
        SystemError: If a wrong Python version is installed.
    """
    # Check correct python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise SystemError("Must use Python 3.6 or newer.")
