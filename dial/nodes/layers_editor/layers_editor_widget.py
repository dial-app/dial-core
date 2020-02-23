# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QDockWidget, QMainWindow

if TYPE_CHECKING:
    from .layers_tree import LayersTreeWidget
    from .model_table import ModelTableWidget
    from PySide2.QtWidgets import QWidget


class LayersEditorWidget(QMainWindow):
    """
    Window for all the model related operations (Create/Modify NN architectures)
    """

    def __init__(
        self,
        layers_tree: "LayersTreeWidget",
        model_table: "ModelTableWidget",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        # Initialize widgets
        self.__model_table = model_table
        self.__model_table.setParent(self)

        self.__layers_tree = layers_tree
        self.__layers_tree.setParent(self)

        self.__dock_layers_tree = QDockWidget(self)

        # Configure interface
        self.__setup_ui()

    def sizeHint(self) -> "QSize":
        return QSize(600, 300)

    def __setup_ui(self):
        # Configure dock widget with layers tree
        self.__dock_layers_tree.setWidget(self.__layers_tree)
        self.__dock_layers_tree.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )

        self.addDockWidget(Qt.LeftDockWidgetArea, self.__dock_layers_tree)

        self.setCentralWidget(self.__model_table)
