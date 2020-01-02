# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Starting point for the application GUI.
"""

import argparse
import signal
import importlib
import sys
from datetime import datetime
from typing import List, Tuple

from dial import __requirements__
from dial.utils import log

LOGGER = log.get_logger(__name__)


def check_python_version():
    """
    Check if Python version installed is correct.
    """
    # Check correct python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise SystemError("Must use Python 3.6 or newer.")

    LOGGER.debug("Python Version: %s", sys.version)


def check_module_installed(module_name: str):
    """
    Check if PySide2 version installed is correct.
    """
    spec = importlib.util.find_spec(module_name)

    if spec is None:
        raise ImportError(
            f"{module_name} module not found!\n\nPlease use "
            f'"pip install --user {module_name}" to install it.'
        )

    LOGGER.debug("%s module found (%s)", spec.name, spec.origin)


def check_required_modules(requirements: List[Tuple[str, str]]):
    """
    Check if the required modules are installed.
    """
    # Warning: Pillow module is actually imported as "PIL", so we have to change its
    # name before checking it
    # Same with "dependency-injector", which is imported name has an underscore
    # (dependency_injector)
    module_imported_name = {
        "Pillow": "PIL",
        "dependency-injector": "dependency_injector",
    }

    required_modules_names = []
    for module_name, _ in __requirements__:
        try:
            required_modules_names.append(module_imported_name[module_name])
        except KeyError:
            continue

    for module_name in required_modules_names:
        check_module_installed(module_name)


def early_init(args: argparse.Namespace):
    """
    Early initialization and checks needed before starting.
    """
    # Init logs system
    log.init_logs(args)

    # Check correct python and module versions
    check_python_version()

    # Check that all the required modules are installed
    check_required_modules(__requirements__)

    # Initialize PySide2
    from PySide2.QtWidgets import QApplication

    QApplication()

    # Handle signals
    signal.signal(signal.SIGINT, signal.SIG_DFL)


def run(args: argparse.Namespace):
    """
    Init all necessary components and show the main window.
    """

    try:
        early_init(args)

    except (ImportError, SystemError) as err:
        log.get_logger(__name__).exception(err)

        from dial.utils import tkinter

        tkinter.showerror(err)
        sys.exit(1)

    # After this point we have checked all dependencies, versions, and all major
    # systems (PySide2) are initialized and ready to work with.

    from dial.gui.mainwindow import MainWindow

    main_window = MainWindow()
    main_window.show()

    from PySide2.QtWidgets import QApplication

    LOGGER.info("Dial.")
    LOGGER.info("Started on %s", datetime.now().ctime())

    return QApplication.exec_()
