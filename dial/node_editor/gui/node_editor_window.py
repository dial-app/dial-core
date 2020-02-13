# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QVBoxLayout, QWidget

from dial.node_editor import Scene

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

        self.show()

    def __setup_ui(self):
        """Sets the UI configuration."""
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)
