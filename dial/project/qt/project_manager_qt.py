# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QAction, QActionGroup, QFileDialog, QMenu, QWidget

from dial.gui.widgets.datasets_list import PredefinedDatasetsList
from dial.gui.widgets.models_list import PredefinedModelLoadersList
from dial.utils import log

from ..project import Project
from ..project_manager import ProjectManager

LOGGER = log.get_logger(__name__)


class ProjectManagerQt(QObject, ProjectManager):
    """
    Project manager with Qt Signals and Dialogs for the project operations.
    """

    dataset_changed = Signal(Project)
    model_changed = Signal(Project)

    project_changed = Signal(Project)

    def __init__(self, default_project: Project, parent=None):
        QObject.__init__(self, parent)
        ProjectManager.__init__(self, default_project)

        self.__projects_menu = QMenu("Projects")
        self.__project_actions_group = QActionGroup(self)
        self.__project_actions_group.setExclusive(True)

        # Add a project action for the default project
        project_action = self.__add_project_to_menu(self.active.name, len(self) - 1)
        project_action.setChecked(True)

        self.project_changed.connect(self.whole_project_changed)

    @property
    def projects_menu(self):
        return self.__projects_menu

    @Slot(Project)
    def whole_project_changed(self, project):
        LOGGER.debug("'whole_project_changed' slot triggered")

        self.dataset_changed.emit(project)
        self.model_changed.emit(project)

    @Slot()
    def load_predefined_dataset(self):
        dataset_loader_dialog = PredefinedDatasetsList.Dialog()

        LOGGER.debug("Opening dialog to select a predefined dataset...")

        accepted = dataset_loader_dialog.exec_()

        if accepted:
            LOGGER.debug("Dataset selected")
            dataset_loader = dataset_loader_dialog.selected_loader()

            super().load_dataset(dataset_loader)

            self.dataset_changed.emit(self.active)
        else:
            LOGGER.debug("Operation cancelled")

    @Slot()
    def load_predefined_model(self):
        model_loader_dialog = PredefinedModelLoadersList.Dialog(parent=self)

        LOGGER.debug("Opening dialog to select a predefined model...")

        accepted = model_loader_dialog.exec_()

        if accepted:
            LOGGER.debug("Model selected")

            model_loader = model_loader_dialog.selected_loader()

            super().load_model(model_loader)
        else:
            LOGGER.debug("Operation cancelled")

    @Slot()
    def new_project(self):
        super().new_project()

        self.__add_project_to_menu(self.active.name, len(self) - 1)

        self.project_changed.emit(self.active)

    @Slot()
    def open_project(self):
        LOGGER.debug("Opening dialog for picking a file...")

        file_path = QFileDialog.getOpenFileName(
            QWidget(), "Open Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for opening: %s", file_path)

        if file_path:
            super().open_project(file_path)

            self.__add_project_to_menu(self.active.name, len(self) - 1)
            self.__project_actions_group.actions()[-1].setChecked(True)

            self.project_changed.emit(self.active)
        else:
            LOGGER.info("Invalid file path. Loading cancelled.")

    @Slot()
    def save_project(self):
        try:
            super().save_project()

        except ValueError:
            LOGGER.warning("Project doesn't have a file path set!")

            self.save_project_as()

    @Slot()
    def save_project_as(self):
        LOGGER.debug("Opening dialog for picking a save file...")

        selected_file_path = QFileDialog.getSaveFileName(
            QWidget(), "Save Dial project", "~", "Dial Files (*.dial)"
        )[0]

        LOGGER.info("File path selected for saving: %s", selected_file_path)

        if selected_file_path:
            super().save_project_as(selected_file_path)

        else:
            LOGGER.info("Invalid file path. Saving cancelled.")

    def set_active_project(self, index):
        super().set_active_project(index)

        self.project_changed.emit(self.active)

    def __add_project_to_menu(self, name, index) -> QAction:
        project_action = QAction(name, self)
        project_action.setCheckable(True)

        project_action.triggered.connect(lambda: self.set_active_project(index))

        self.__project_actions_group.addAction(project_action)
        self.__projects_menu.addAction(project_action)

        return project_action
