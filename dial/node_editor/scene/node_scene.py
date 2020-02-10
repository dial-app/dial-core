# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .graphics_node_scene import GraphicsNodeScene


class NodeScene:
    def __init__(self):
        self.nodes = []
        self.edges = []

        self.graphics_scene = GraphicsNodeScene(self)

    def addNode(self, node):
        self.nodes.append(node)
        self.graphics_scene.addItem(node.graphics_node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        self.nodes.remove(node)
        self.graphics_scene.removeItem(node.graphics_node)

    def removeEdge(self, edge):
        self.edges.remove(edge)
