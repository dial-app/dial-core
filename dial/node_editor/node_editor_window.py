# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QBrush, QPen
from PySide2.QtWidgets import QApplication, QGraphicsItem, QVBoxLayout, QWidget

from .node import Node
from .node_editor_view import NodeEditorView
from .scene import Scene


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.styleSheet_filename = "qss/nodestyle.qss"
        self.loadStylesheet(self.styleSheet_filename)

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView()
        self.__node_editor_scene = Scene()

        node = Node("My Awesome Node")

        self.__node_editor_scene.addNode(node)

        self.__node_editor_view.setScene(self.__node_editor_scene.graphics_scene)

        self.__setup_ui()

        self.show()  # Necessary (Otherwise won't display any items)

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def addDebugContent(self):
        green_brush = QBrush(Qt.green)
        outline_pen = QPen(Qt.black)
        outline_pen.setWidth(2)

        rect = self.__node_editor_scene.grScene.addRect(
            -100, -100, 100, 100, outline_pen, green_brush
        )

        rect.setFlag(QGraphicsItem.ItemIsMovable)

    def loadStylesheet(self, filename):
        print("Style loading", filename)

        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)

        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))
