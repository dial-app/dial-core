# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""


from PySide2.QtCore import QPointF

from dial.node_editor_2.socket import Socket

from .graphics_node import GraphicsNode
from .node_content_widget import NodeContentWidget


class Node:
    def __init__(self, title="Undefined Node", inputs=None, outputs=None):
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

    def pos(self) -> QPointF:
        return self.graphics_node.pos()

    def setPos(self, x, y):
        self.graphics_node.setPos(x, y)

    def updateConnectedEdges(self):
        def update_sockets(sockets):
            for socket in sockets:
                if socket.edge:
                    socket.edge.graphics_edge.updatePositions()

        update_sockets(self.inputs)
        update_sockets(self.outputs)
