"""
Starting point for the application GUI.
"""

import sys


def __early_init(argv):
    """
    Early initialization and checks needed before starting.
    """

    # Check correct python version
    if sys.version_info[0] < 3 or sys.version_info[1] < 6:
        raise SystemError("Must use Python 3.6 or newer.")

    # Init logs system
    from dial.utils import log

    log.init_logs()

    # Check if PySide2 is installed and init it
    try:
        from PySide2.QtWidgets import QApplication

        QApplication(argv)

    except ImportError:
        raise ImportError(
            'Pyside2 module not found. Please use "pip install --user PySide2" '
            "to install it."
        )


def run(argv):
    """
    Init all necessary components and show the main window.
    """

    try:
        __early_init(argv)
    except Exception as err:
        print(err)  # TODO: Change with logging
        showinfo("Error", err)
        sys.exit(126)

    # After this point we have checked all dependencies, versions, and all major systems
    # (PySide2) are initialized and ready to work with.

    from dial.gui.mainwindow import MainWindow

    main_window = MainWindow()
    main_window.show()

    from PySide2.QtWidgets import QApplication

    return QApplication.exec_()
