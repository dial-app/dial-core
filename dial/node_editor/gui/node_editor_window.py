# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QMenu, QVBoxLayout, QWidget

from dial.node_editor import Scene

from .graphics_scene import GraphicsScene
from .node_editor_view import NodeEditorView

if TYPE_CHECKING:
    from PySide2.QtWidgets import QTabWidget
    from PySide2.QtGui import QContextMenuEvent


class NodeEditorWindow(QWidget):
    def __init__(self, tabs_widget: "QTabWidget", parent: "QWidget" = None):
        super().__init__(parent)

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView(tabs_widget, parent=self)
        self.__scene = Scene()
        self.__graphics_scene = GraphicsScene(self.__scene, parent=self)

        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__setup_ui()

        # self.add_example_nodes()

        self.show()

    def __setup_ui(self):
        """Sets the UI configuration."""
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def contextMenuEvent(self, event: "QContextMenuEvent"):
        menu = QMenu(self)

        # TODO: Finish
        menu.popup(event.globalPos())
        menu.addAction("Open")

    # # TODO: Remove from here
    # def add_example_nodes(self):
    #     dataset_node = NodeFactorySingleton().get_node("Dataset Editor")
    #     layers_node = NodeFactorySingleton().get_node("Layers Editor")
    #     compiler_node = NodeFactorySingleton().get_node("Model Compiler")

    #     # self.__scene.add_node(my_node)
    #     self.__scene.add_node(dataset_node)
    #     self.__scene.add_node(layers_node)
    #     self.__scene.add_node(compiler_node)
