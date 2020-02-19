# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QVBoxLayout, QWidget

from dial.node_editor import Scene
from dial.nodes.dataset_editor import DatasetEditorNodeFactory
from dial.nodes.layers_editor import LayersEditorNodeFactory
from dial.nodes.model_compiler import ModelCompilerNodeFactory

from .graphics_scene import GraphicsScene
from .node_editor_view import NodeEditorView


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView()
        self.__scene = Scene()
        self.__graphics_scene = GraphicsScene(self.__scene)

        self.__node_editor_view.setScene(self.__graphics_scene)

        self.__setup_ui()

        self.add_example_nodes()

        self.show()

    def __setup_ui(self):
        """Sets the UI configuration."""
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def add_example_nodes(self):
        # my_node = Node(title="Example Node 1")

        dataset_node = DatasetEditorNodeFactory()
        layers_node = LayersEditorNodeFactory()
        compiler_node = ModelCompilerNodeFactory()

        # self.__scene.add_node(my_node)
        self.__scene.add_node(dataset_node)
        self.__scene.add_node(layers_node)
        self.__scene.add_node(compiler_node)
