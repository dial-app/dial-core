# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QMainWindow, QTabWidget

from dial import __version__
from dial.project import DialProjectManager
from dial.utils import log

LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(
        self,
        project_manager,
        datasets_window,
        models_window,
        compile_window,
        menubar,
        logger_dialog,
        parent=None,
    ):
        super().__init__(parent)

        # Initialize logging first (Order is important)
        self.__logger_dialog = logger_dialog

        self.__setup_logger_dialog()

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__main_menu_bar = menubar
        self.__main_menu_bar.setParent(self)

        self.__tabs_widget = QTabWidget(self)

        self.__datasets_window = datasets_window
        self.__datasets_window.setParent(self)

        self.__models_window = models_window
        self.__models_window.setParent(self)

        self.__compile_window = compile_window
        self.__compile_window.setParent(self)

        # Configure ui
        self.__setup_ui()

        project_manager = DialProjectManager()
        self.__main_menu_bar.addMenu(project_manager.projects_menu)

        # Connect signals
        self.__main_menu_bar.new_project.connect(project_manager.new_project)
        self.__main_menu_bar.open_project.connect(project_manager.open_project)
        self.__main_menu_bar.save_project.connect(project_manager.save_project)
        self.__main_menu_bar.save_project_as.connect(project_manager.save_project_as)

        # TODO: Think: Connect to project_manager instead of windows??
        self.__main_menu_bar.open_predefined_dataset.connect(
            self.__datasets_window.load_predefined_dataset
        )

        # TODO: ^^^^
        self.__main_menu_bar.open_predefined_model.connect(
            self.__models_window.load_predefined_model
        )

        self.__main_menu_bar.quit.connect(QApplication.quit)
        self.__main_menu_bar.toggle_log_window.connect(self.__toggle_log_window)

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
        self.__tabs_widget.addTab(self.__datasets_window, "Datasets")
        self.__tabs_widget.addTab(self.__models_window, "Models")
        self.__tabs_widget.addTab(self.__compile_window, "Compile")

    def sizeHint(self):
        return QSize(800, 600)

    def __toggle_log_window(self):
        self.__logger_dialog.show()
