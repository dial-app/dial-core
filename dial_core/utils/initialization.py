# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
"""
Functions to check that python versions, libraries... used by the program are correct.
"""


import argparse
import signal
import sys
from importlib.util import find_spec
from typing import List, Tuple

from dial_core import __description__, __requirements__
from dial_core.utils import log
from dial_core.utils.log import DEBUG, log_on_end

LOGGER = log.get_logger(__name__)


def initialize_application(args: "argparse.Namespace"):
    """Performs all the necessary steps before running the application. This checks
    python version, installed modules, graphics configurations, initialize logging
    system...

    Raises:
        ImportError: If couldn't import a necessary module.
        SystemError: If the Python version isn't compatible.
    """
    try:
        __non_gui_initialization(args)
        __gui_initialization(args)

    except (ImportError, SystemError) as err:
        LOGGER.exception(err)

        from dial_core.utils import tkinter

        tkinter.showerror(str(err))
        sys.exit(1)


def __non_gui_initialization(args: "argparse.Namespace"):
    """Performs all the necessary initialization before the GUI initialization."""
    # Init logs system
    log.init_logs(args)

    # Check correct python and module versions
    check_python_version()

    # Check that all the required modules are installed
    check_required_modules(__requirements__)

    # State the signals handled by this application
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def __gui_initialization(args: "argparse.Namespace"):
    """Performs all the initialization of the GUI components.

    Args:
        args: App configuration namespace."""
    # Initialize PySide2
    from PySide2.QtWidgets import QApplication

    QApplication()

    # TODO: Solve this import issue
    import dial.nodes  # noqa


def parse_args(sys_args: List):
    """Parses the system arguments (sys.arv), returning the app configuration.

    Args:
        sys_args: List of arguments to parse.
    """
    return get_arg_parser().parse_args(sys_args)


def get_arg_parser() -> "argparse.ArgumentParser":
    """
    Returns:
        An argument parser for this application.
    """
    parser = argparse.ArgumentParser(prog="dial", description=__description__)

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


@log_on_end(DEBUG, "{result.name} module found ({result.origin})", logger=LOGGER)
def check_module_installed(module_name: str):
    """
    Check if PySide2 version installed is correct.

    Raises:
        ImportError: If the module is not installed.

    Returns:
        A module specification object if found.
    """
    spec = find_spec(module_name)

    if spec is None:
        raise ImportError(
            f"{module_name} module not found!\n\nPlease use "
            f'"pip install --user {module_name}" to install it.'
        )

    return spec


def check_required_modules(requirements: List[Tuple[str, str]]):
    """
    Check if the required modules are installed.

    Raises:
        ImportError: If the module is not installed.
    """
    # Warning: Pillow module is actually imported as "PIL", so we have to change its
    # name before checking it
    # Same with "dependency-injector", which is imported name has an underscore
    # (dependency_injector)
    module_imported_name = {
        "Pillow": "PIL",
        "dependency-injector": "dependency_injector",
    }

    # Iterate through each module
    for module_name, _ in requirements:
        try:
            check_module_installed(module_imported_name[module_name])
        except KeyError:
            check_module_installed(module_name)
