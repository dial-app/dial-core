# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QAction, QMenuBar

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget
    from dial.gui.widgets.menus import FileMenu


class MainMenuBar(QMenuBar):
    """
    Top menu bar for the main window.
    """

    open_predefined_dataset = Signal()

    open_predefined_model = Signal()

    toggle_log_window = Signal()

    def __init__(self, file_menu: "FileMenu", parent: "QWidget" = None):
        super().__init__(parent)

        self.__file_menu = file_menu

        self.__create_actions()
        self.__create_menus()

    def __create_actions(self):
        self._open_predefined_dataset_act = QAction("Open predefined dataset...", self)
        self._open_predefined_dataset_act.triggered.connect(
            self.open_predefined_dataset
        )

        self._open_predefined_model_act = QAction("Open predefined model...", self)
        self._open_predefined_model_act.triggered.connect(self.open_predefined_model)

        self._show_log_act = QAction("Show log", self)
        self._show_log_act.triggered.connect(self.toggle_log_window)

    def __create_menus(self):
        # File menu
        self._file_menu = self.addMenu(self.__file_menu)

        # Datasets menu
        self._dataset_menu = self.addMenu("&Dataset")
        self._dataset_menu.addAction(self._open_predefined_dataset_act)

        # Models menu
        self._model_menu = self.addMenu("&Model")
        self._model_menu.addAction(self._open_predefined_model_act)

        # Windows menu
        self._windows_menu = self.addMenu("&Windows")
        self._windows_menu.addAction(self._show_log_act)
