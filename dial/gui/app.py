"""
Starting point for the application GUI.
"""

from PySide2.QtWidgets import QApplication

from dial.gui.mainwindow import MainWindow
from dial.utils import log


def __early_init(argv):
    """
    Early initialization and checks needed before starting.
    """

    # Start logs system
    log.init_logs()

    # Start Qt module
    QApplication(argv)


def run(argv):
    """
    Init all necessary components and show the main window.
    """

    __early_init(argv)

    main_window = MainWindow()
    main_window.show()

    return QApplication.exec_()
