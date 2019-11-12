"""
Menu bar for the main window.
"""

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QAction, QMenuBar


class MainMenuBar(QMenuBar):
    quit = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self._create_actions()
        self._create_menus()

    def _create_actions(self):
        self._quit_act = QAction("Quit", self)
        self._quit_act.triggered.connect(self.quit)

    def _create_menus(self):
        self._file_menu = self.addMenu("&File")

        self._file_menu.addAction(self._quit_act)
