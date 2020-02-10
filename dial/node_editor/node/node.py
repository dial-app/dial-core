# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""


from dial.node_editor.socket import Socket

from .graphics_node import GraphicsNode
from .node_content_widget import NodeContentWidget


class Node:
    def __init__(self, title="Undefined Node", inputs=None, outputs=None):
        self.scene = None

        self.title = title

        self.inputs = []
        self.outputs = []

        if inputs:
            for i, socket in enumerate(inputs):
                socket.node = self
                socket.index = i
                socket.position = Socket.Position.LeftTop

                self.inputs.append(socket)

        if outputs:
            for i, socket in enumerate(outputs):
                socket.node = self
                socket.index = i
                socket.position = Socket.Position.RightTop

                self.outputs.append(socket)

        # Node components
        self.content = NodeContentWidget()
        self.graphics_node = GraphicsNode(self)
