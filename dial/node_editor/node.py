# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""


from .graphics_node import GraphicsNode
from .node_content_widget import NodeContentWidget


class Node:
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.content = NodeContentWidget()
        self.grNode = GraphicsNode(self)

        self.scene.addNode(self)

        self.inputs = []
        self.outpus = []
