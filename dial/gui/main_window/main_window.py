# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QMainWindow, QTabBar, QTabWidget

from dial import __version__
from dial.gui.node_editor import NodeEditorWindow
from dial.gui.widgets.menus import FileMenu
from dial.utils import log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """The main window for the program."""

    def __init__(
        self, menubar_factory, logger_dialog, project_manager, parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize logging first (Order is important)
        self.__logger_dialog = logger_dialog

        self.__setup_logger_dialog()

        # Initialize widgets
        self.__project_manager = project_manager

        self.__main_menu_bar = menubar_factory(
            file_menu=FileMenu(self.__project_manager)
        )
        self.__main_menu_bar.setParent(self)

        self.__tabs_widget = QTabWidget(self)
        self.__node_editor = NodeEditorWindow(
            tabs_widget=self.__tabs_widget,
            project_manager=self.__project_manager,
            parent=self,
        )

        # Configure ui
        self.__setup_ui()
        self.__main_menu_bar.toggle_log_window.connect(self.__toggle_log_window)

    def sizeHint(self) -> "QSize":
        """Returns the size of the main window."""
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

        self.__tabs_widget.setMovable(True)
        self.__tabs_widget.setTabsClosable(True)

        self.__tabs_widget.tabCloseRequested.connect(
            lambda index: self.__tabs_widget.removeTab(index)
        )

        self.__tabs_widget.addTab(self.__node_editor, "Editor")

        # Remove "delete" button from the tab
        self.__tabs_widget.tabBar().tabButton(0, QTabBar.RightSide).deleteLater()
        self.__tabs_widget.tabBar().setTabButton(0, QTabBar.RightSide, None)

    def __toggle_log_window(self):
        self.__logger_dialog.show()
