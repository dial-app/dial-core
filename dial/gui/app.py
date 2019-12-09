"""
Starting point for the application GUI.
"""

import sys


def __check_python_version():
    """
    Check if Python version installed is correct.
    """
    # Check correct python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise SystemError("Must use Python 3.6 or newer.")


def __check_pyside2_version():
    """
    Check if PySide2 version installed is correct.
    """
    try:
        import PySide2

        # TODO: Check minimal working PySide2 version

    except ImportError:
        raise ImportError(
            'Pyside2 module not found. Please use "pip install --user PySide2" '
            "to install it."
        )


def __early_init(argv):
    """
    Early initialization and checks needed before starting.
    """

    # Init logs system
    from dial.utils import log

    __check_python_version()
    __check_pyside2_version()

    log.init_logs()

    # Check if PySide2 is installed and init it
    from PySide2.QtWidgets import QApplication

    QApplication(argv)


def run(argv):
    """
    Init all necessary components and show the main window.
    """

    try:
        __early_init(argv)

        # After this point we have checked all dependencies, versions, and all major
        # systems (PySide2) are initialized and ready to work with.

        from dial.gui.mainwindow import MainWindow

        main_window = MainWindow()
        main_window.show()

        from PySide2.QtWidgets import QApplication

        return QApplication.exec_()

    except Exception as err:
        print(err)

        from dial.utils import tkinter

        tkinter.showerror("Error", err)
        sys.exit(1)
