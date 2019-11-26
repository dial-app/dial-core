# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget

from tfg.mainwindow.mainmenubar import MainMenuBar
from tfg.utils import log
from tfg.widgets.windows import DatasetsWindow


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._main_menu_bar = MainMenuBar(self)
        self._tabs_widget = QTabWidget(self)

        self._setup()

        log.mainwindow.info("Program Initialized")

    def _setup(self):
        # Widget configuration
        self.setWindowTitle("TFG")

        self.setMenuBar(self._main_menu_bar)

        self.setCentralWidget(self._tabs_widget)

        # Tab widget
        self._tabs_widget.addTab(DatasetsWindow(self), "Datasets")

        # Connections
        self._main_menu_bar.quit.connect(QApplication.quit)
        self._main_menu_bar.toggle_log_window.connect(self._toggle_log_window)

    def sizeHint(self):
        return QSize(800, 600)

    def _toggle_log_window(self):
        dialog = log.LoggerTextboxDialog(self)

        dialog.show()
