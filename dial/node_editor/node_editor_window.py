# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QFile
from PySide2.QtWidgets import QApplication, QVBoxLayout, QWidget

from .edge import Edge, GraphicsEdgeBezier
from .node import Node
from .node_editor_view import NodeEditorView
from .scene import NodeScene
from .socket import Socket


class NodeEditorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.styleSheet_filename = "qss/nodestyle.qss"
        self.loadStylesheet(self.styleSheet_filename)

        self.__main_layout = QVBoxLayout()

        self.__node_editor_view = NodeEditorView()
        self.__node_editor_scene = NodeScene()

        self.addNodes()

        self.__node_editor_view.setScene(self.__node_editor_scene.graphics_scene)

        self.__setup_ui()

        self.show()  # Necessary (Otherwise won't display any items)

    def addNodes(self):
        node1 = Node(
            "My Awesome Node 1", inputs=[Socket(), Socket()], outputs=[Socket()]
        )
        node2 = Node(
            "My Awesome Node 2", inputs=[Socket(), Socket()], outputs=[Socket()]
        )
        node3 = Node(
            "My Awesome Node 3", inputs=[Socket(), Socket()], outputs=[Socket()]
        )

        node1.setPos(0, 0)
        node2.setPos(-350, -250)
        node3.setPos(450, -300)

        self.__node_editor_scene.addNode(node1)
        self.__node_editor_scene.addNode(node2)
        self.__node_editor_scene.addNode(node3)

        edge = Edge(node1.outputs[0], node2.inputs[0])
        edge = Edge(node1.outputs[0], node2.inputs[0], edge_type=GraphicsEdgeBezier)
        self.__node_editor_scene.addEdge(edge)

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__node_editor_view)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def loadStylesheet(self, filename):
        print("Style loading", filename)

        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)

        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding="utf-8"))
