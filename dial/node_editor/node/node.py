# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""


from .graphics_node import GraphicsNode
from .node_content_widget import NodeContentWidget


class Node:
    def __init__(self, title="Undefined Node"):
        self.scene = None

        self.title = title

        self.inputs = []
        self.outpus = []

        # Node components
        self.content = NodeContentWidget()
        self.graphics_node = GraphicsNode(self)
