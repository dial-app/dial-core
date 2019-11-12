# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""

from PySide2.QtWidgets import QApplication, QMainWindow

from tfg.utils import log

from .mainmenubar import MainMenuBar


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._main_menu_bar = MainMenuBar(self)

        self._setup()

        log.mainwindow.info("Program Initialized")

    def _setup(self):
        self.setWindowTitle("TFG")

        self.setMenuBar(self._main_menu_bar)

        self._main_menu_bar.quit.connect(QApplication.quit)
