# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QDockWidget, QMainWindow


class LayersEditorWidget(QMainWindow):
    """
    Window for all the model related operations (Create/Modify NN architectures)
    """

    def __init__(
        self, layers_tree, model_table, parent=None,
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

    def sizeHint(self):
        return QSize(600, 300)

    def __setup_ui(self):
        # Configure dock widget with layers tree
        self.__dock_layers_tree.setWidget(self.__layers_tree)
        self.__dock_layers_tree.setFeatures(
            QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable
        )

        self.addDockWidget(Qt.LeftDockWidgetArea, self.__dock_layers_tree)

        self.setCentralWidget(self.__model_table)
