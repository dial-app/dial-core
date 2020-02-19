# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget

from dial import __version__
from dial.node_editor.gui import NodeEditorWindow
from dial.utils import log

LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(
        self, menubar, logger_dialog, parent=None,
    ):
        super().__init__(parent)

        # Initialize logging first (Order is important)
        self.__logger_dialog = logger_dialog

        self.__setup_logger_dialog()

        # Initialize widgets
        self.__main_menu_bar = menubar
        self.__main_menu_bar.setParent(self)

        self.__node_editor = NodeEditorWindow(parent=self)

        self.__tabs_widget = QTabWidget(self)

        # Configure ui
        self.__setup_ui()
        self.__main_menu_bar.quit.connect(QApplication.quit)
        self.__main_menu_bar.toggle_log_window.connect(self.__toggle_log_window)

    def sizeHint(self):
        return QSize(1000, 800)

    def __setup_logger_dialog(self):
        # Add the logger window as a new log handler
        log.add_handler_to_root(self.__logger_dialog.handler())

        # Write on the window all the previous log messages
        self.__logger_dialog.textbox.set_plain_text(log.LOG_STREAM.getvalue())

    def __setup_ui(self):
        # Set window title
        self.setWindowTitle("Dial " + __version__)

        # Configure menu and status bars
        self.setMenuBar(self.__main_menu_bar)
        self.setStatusBar(self.statusBar())

        self.setCentralWidget(self.__tabs_widget)

        # Configure Tabs widget
        self.__tabs_widget.addTab(self.__node_editor, "Editor")

    def __toggle_log_window(self):
        self.__logger_dialog.show()
