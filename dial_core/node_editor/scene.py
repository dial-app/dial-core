# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers

from dial_core.utils.log import DEBUG, log_on_end

if TYPE_CHECKING:
    from .node import Node


class Scene:
    """The Scene class provides a data container for storing the Nodes that form a graph.

    Attributes:
        nodes: The list of nodes currently on the scene.
    """

    def __init__(self):
        self.__nodes: List["Node"] = []

    @property
    def nodes(self) -> List["Node"]:
        """Returns a list with all the nodes on the scene."""
        return self.__nodes

    @log_on_end(DEBUG, "{node} added to the scene.")
    def add_node(self, node: "Node"):
        """Adds a new node to the scene."""
        self.nodes.append(node)

    def remove_node(self, node: "Node"):
        try:
            self.nodes.remove(node)
        except ValueError:
            pass

    def __repr__(self):
        output = ""

        for node in self.__nodes:
            output += f"Node {node!r} has:\n"

            for port in list(node.inputs.values()) + list(node.outputs.values()):
                output += f"\tPort: {port!r}\n"
                for connection in port.connections:
                    output += f"\t\t- Connected to: {connection!r}\n"

        return output

    def __iter__(self):
        return iter(self.__nodes)

    def __eq__(self, other):
        return self.nodes == other.nodes


SceneFactory = providers.Factory(Scene)
