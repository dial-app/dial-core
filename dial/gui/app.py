"""
Starting point for the application GUI.
"""

import importlib
import sys
from datetime import datetime

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


def early_init(argv):
    """
    Early initialization and checks needed before starting.
    """

    # Init logs system
    log.init_logs()

    # Check correct python and module versions
    check_python_version()

    # Warning: Pillow module is actually imported as "PIL", so we have to change its
    # name before checking it
    required_modules_names = [
        module[0].replace("Pillow", "PIL") for module in __requirements__
    ]

    for module_name in required_modules_names:
        check_module_installed(module_name)

    # Initialize PySide2
    from PySide2.QtWidgets import QApplication

    QApplication(argv)


def run(argv):
    """
    Init all necessary components and show the main window.
    """

    try:
        early_init(argv)

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
