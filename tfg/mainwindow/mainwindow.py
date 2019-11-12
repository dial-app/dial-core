# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from tfg.utils import log


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("TFG")

        self._add_widgets()

        log.mainwindow.info("Program initialized.")

    def _add_widgets(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
