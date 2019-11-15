# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Menu bar for the main window.
"""

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QAction, QMenuBar


class MainMenuBar(QMenuBar):
    quit = Signal()
    toggle_log_window = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self._create_actions()
        self._create_menus()

    def _create_actions(self):
        # Quit act
        self._quit_act = QAction("Quit", self)
        self._quit_act.triggered.connect(self.quit)

        # Show log window act
        self._show_log_act = QAction("Show log", self)
        self._show_log_act.triggered.connect(self.toggle_log_window)

    def _create_menus(self):
        # File menu
        self._file_menu = self.addMenu("&File")
        self._file_menu.addAction(self._quit_act)

        # Windows menu
        self._windows_menu = self.addMenu("Windows")
        self._windows_menu.addAction(self._show_log_act)
