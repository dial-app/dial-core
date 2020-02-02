# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QFileDialog, QWidget

from dial.utils import log

from ..project import Project
from ..project_manager import ProjectManager

LOGGER = log.get_logger(__name__)


class ProjectManagerQt(QObject, ProjectManager):
    """
    Project manager with Qt Signals and Dialogs for the project operations.
    """

    def __init__(self, default_project: Project, parent=None):
        QObject.__init__(self, parent)
        ProjectManager.__init__(self, default_project)

    @Slot()
    def new_project(self):
        super().new_project()

    @Slot()
    def open_project(self):
        LOGGER.debug("Opening dialog for picking a file...")

        file_path = QFileDialog.getOpenFileName(
            QWidget(), "Open Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for opening: %s", file_path)

        if file_path:
            super().open_project(file_path)
        else:
            LOGGER.info("Invalid file path. Loading cancelled.")

    @Slot()
    def save_project(self):
        try:
            super().save_project()
        except ValueError:
            LOGGER.warning("Project doesn't have a file path set!")
            self.__save_project_as()

    @Slot()
    def save_project_as(self):
        LOGGER.debug("Opening dialog for picking a save file...")

        file_path = QFileDialog.getSaveFileName(
            QWidget(), "Save Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for saving: %s", file_path)

        if file_path:
            super().save_project_as(file_path)
        else:
            LOGGER.info("Invalid file path. Saving cancelled.")
