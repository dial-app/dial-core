# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .node_editor_scene import NodeEditorScene


class Scene:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.grScene = NodeEditorScene(self)

        self.__setup_ui()

    def __setup_ui(self):
        self.grScene.setScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)

    def removeEdge(self, edge):
        self.edges.remove(edge)
