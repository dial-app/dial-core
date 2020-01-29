# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the model related operations (Create/Modify NN architectures)
"""

from PySide2.QtWidgets import QHBoxLayout, QSplitter, QWidget

from dial.gui.widgets import PredefinedModelLoadersList
from dial.project import ProjectInstance
from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelsWindow(QWidget):
    """
    """

    def __init__(self, layers_tree: QWidget, model_table: QWidget, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__model_table = model_table
        self.__model_table.setParent(self)
        self.__layers_tree = layers_tree
        self.__layers_tree.setParent(self)

        self.__main_layout = QHBoxLayout()

        # Configure interface
        self.__setup_ui()

        # Connect signals
        ProjectInstance().model_changed.connect(self.__update_from_project)

    def __setup_ui(self):
        splitter = QSplitter()

        self.__model_table.sizePolicy().setHorizontalStretch(5)

        splitter.addWidget(self.__layers_tree)
        splitter.addWidget(self.__model_table)

        self.__main_layout.addWidget(splitter)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def load_predefined_model(self):
        model_loader_dialog = PredefinedModelLoadersList.Dialog(parent=self)

        LOGGER.debug("Opening dialog to select a predefined model...")

        accepted = model_loader_dialog.exec_()

        if accepted:
            LOGGER.debug("Model selected")

            model_loader = model_loader_dialog.selected_loader()

            project = ProjectInstance()
            project.model.load_model(model_loader)
        else:
            LOGGER.debug("Operation cancelled")

    def __update_from_project(self, project):
        LOGGER.debug("Updating model from project")
        self.__model_table.set_model(project.model.model)
