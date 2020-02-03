# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the model related operations (Create/Modify NN architectures)
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDockWidget, QMainWindow, QWidget

from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelsWindow(QMainWindow):
    """
    """

    def __init__(
        self, project_manager, layers_tree: QWidget, model_table: QWidget, parent=None
    ):
        super().__init__(parent)

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__model_table = model_table
        self.__model_table.setParent(self)

        self.__layers_tree = layers_tree
        self.__layers_tree.setParent(self)

        self.__dock_layers_tree = QDockWidget(self)

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__project_manager.model_changed.connect(self.__update_from_project)

    def __setup_ui(self):
        # Configure dock widget with layers tree
        self.__dock_layers_tree.setWidget(self.__layers_tree)
        self.__dock_layers_tree.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )
        self.__dock_layers_tree.setWindowTitle("Layers")

        self.addDockWidget(Qt.LeftDockWidgetArea, self.__dock_layers_tree)

        self.setCentralWidget(self.__model_table)

    def __update_from_project(self, project):
        self.__model_table.set_model(project.model.layers)
