# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the model related operations (Create/Modify NN architectures)
"""

from PySide2.QtWidgets import QGridLayout, QWidget

from dial.project import ProjectInstance
from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelsWindow(QWidget):
    """
    """

    def __init__(self, model_table, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__model_table = model_table

        self.__main_layout = QGridLayout()

        # Configure interface
        self.__setup_ui()

        # Connect signals
        ProjectInstance().project_changed.connect(self.__update_from_project)

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__model_table, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def load_predefined_model(self):
        LOGGER.debug("Opening dialog to select a predefined model...")

    def __update_from_project(self, project):
        # self.__model_table.set_model(project.model)
        pass
