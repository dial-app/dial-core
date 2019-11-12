# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QVBoxLayout

from tfg.utils import log


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("TFG")

        log.mainwindow.info("Program Initialized")
