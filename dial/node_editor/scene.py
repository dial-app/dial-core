# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List

from PySide2.QtCore import QObject, Signal

from dial.utils.log import DEBUG, log_on_end

if TYPE_CHECKING:
    from .node import Node


class Scene(QObject):
    node_added = Signal("Node")

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__nodes = []

    @property
    def nodes(self) -> List["Node"]:
        """Returns all the nodes on the scene."""
        return self.__nodes

    @log_on_end(DEBUG, "{node} added to the scene.")
    def add_node(self, node: "Node"):
        """Adds a new node to the scene."""
        self.nodes.append(node)

        self.node_added.emit(node)
