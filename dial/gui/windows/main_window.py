# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""The main window for the program."""
from PySide2.QtCore import QSize
from PySide2.QtWidgets import QApplication, QFileDialog, QMainWindow, QTabWidget

from dial import __version__
from dial.project import ProjectInstance
from dial.utils import log

LOGGER = log.get_logger(__name__)


class MainWindow(QMainWindow):
    """
    The main window for the program.
    """

    def __init__(
        self,
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

        # Connect signals
        self.__main_menu_bar.open_project.connect(self.__open_project)
        self.__main_menu_bar.save_project.connect(self.__save_project)
        self.__main_menu_bar.save_project_as.connect(self.__save_project_as)

        self.__main_menu_bar.open_predefined_dataset.connect(
            self.__datasets_window.load_predefined_dataset
        )

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

    def __open_project(self):
        LOGGER.debug("Opening dialog for picking a file...")

        file_path = QFileDialog.getOpenFileName(
            self, "Open Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for opening: %s", file_path)

        if file_path:
            ProjectInstance().load(file_path)
        else:
            LOGGER.info("Invalid file path. Loading cancelled.")

    def __save_project(self):
        try:
            ProjectInstance().save()
        except ValueError:
            LOGGER.warning("Project doesn't have a file path set!")
            self.__save_project_as()

    def __save_project_as(self):
        LOGGER.debug("Opening dialog for picking a save file...")

        file_path = QFileDialog.getSaveFileName(
            self, "Save Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for saving: %s", file_path)

        if file_path:
            ProjectInstance().save_as(file_path)
        else:
            LOGGER.info("Invalid file path. Saving cancelled.")
