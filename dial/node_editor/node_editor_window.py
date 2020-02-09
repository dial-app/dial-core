# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt
from PySide2.QtGui import QBrush, QPen
from PySide2.QtWidgets import QGraphicsItem, QVBoxLayout, QWidget

from dial.node_editor import NodeEditorScene, NodeEditorView


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView()
        self.__node_editor_scene = NodeEditorScene()

        self.__node_editor_view.setScene(self.__node_editor_scene)

        self.__setup_ui()

        self.addDebugContent()

        self.show()  # Necessary (Otherwise won't display any items)

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def addDebugContent(self):
        green_brush = QBrush(Qt.green)
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(2)

        rect = self.__node_editor_scene.addRect(
            -100, -100, 100, 100, outline_pen, green_brush
        )

        rect.setFlag(QGraphicsItem.ItemIsMovable)
