# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Starting point for the application GUI.
"""

import argparse
import signal
import sys
from datetime import datetime

from dial import __requirements__
from dial.utils import initialization, log

LOGGER = log.get_logger(__name__)


def early_init(args: argparse.Namespace):
    """
    Early initialization and checks needed before starting.
    """
    # Init logs system
    log.init_logs(args)

    # Check correct python and module versions
    initialization.check_python_version()

    # Check that all the required modules are installed
    initialization.check_required_modules(__requirements__)

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

        tkinter.showerror(str(err))
        sys.exit(1)

    # After this point we have checked that all dependencies, versions, and all major
    # systems (PySide2) are initialized and ready to work with.

    from dial.gui.windows import Windows

    main_window = Windows.Main()
    main_window.show()

    from PySide2.QtWidgets import QApplication

    LOGGER.debug("Command Line Arguments: %s", args)
    LOGGER.info("Dial.")
    LOGGER.info("Started on %s", datetime.now().ctime())

    return QApplication.exec_()
