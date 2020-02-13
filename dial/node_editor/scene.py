# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject, Signal

from dial.utils.log import DEBUG, log_on_end

from .node import Node


class Scene(QObject):
    node_added = Signal(Node)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__nodes = []

    @property
    def nodes(self):
        """Returns all the nodes on the scene."""
        return self.__nodes

    @log_on_end(DEBUG, "{node} added to the scene.")
    def add_node(self, node: Node):
        """Adds a new node to the scene."""
        self.nodes.append(node)

        self.node_added.emit(node)
