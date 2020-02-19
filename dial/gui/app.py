# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Starting point for the application GUI.
"""

import argparse
from datetime import datetime

from PySide2.QtWidgets import QApplication

from dial.gui.windows import Windows
from dial.utils import log


def run(args: argparse.Namespace):
    """
    Show the main window and start the application.

    Warning:
        The system must be initialized before calling this function.

    See Also:
        `dial.utils.initialization.initialize_application`
    """

    main_window = Windows.Main()
    main_window.show()

    log.module_logger().debug("Command Line Arguments: %s", args)
    log.module_logger().info("Dial.")
    log.module_logger().info("Started on %s", datetime.now().ctime())

    return QApplication.exec_()
