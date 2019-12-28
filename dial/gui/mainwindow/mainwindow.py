# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""
from dial import __version__
from dial.gui.mainwindow.mainmenubar import MainMenuBar
from dial.gui.widgets.log import LoggerDialog
from dial.gui.widgets.windows import DatasetsWindow
from dial.utils import log
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_menu_bar = MainMenuBar(self)
        self.__tabs_widget = QTabWidget(self)
        self.__logger_dialog = LoggerDialog(self)

        self.__setup_logger_dialog()
        self.__setup_ui()

    def __setup_logger_dialog(self):
        log.add_handler_to_root(self.__logger_dialog.handler())
        self.__logger_dialog.textbox.set_plain_text(log.LOG_STREAM.getvalue())

    def __setup_ui(self):
        # Widget configuration
        self.setWindowTitle("Dial " + __version__)

        self.setMenuBar(self.__main_menu_bar)
        self.setStatusBar(self.statusBar())

        self.setCentralWidget(self.__tabs_widget)

        # Tab widget
        self.__tabs_widget.addTab(DatasetsWindow(self), "Datasets")

        # Connections
        self.__main_menu_bar.quit.connect(QApplication.quit)
        self.__main_menu_bar.toggle_log_window.connect(self.__toggle_log_window)

    def sizeHint(self):
        return QSize(800, 600)

    def __toggle_log_window(self):
        self.__logger_dialog.show()
