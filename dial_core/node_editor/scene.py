# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
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

    def duplicate_nodes(self, nodes: List["Node"]) -> List["Node"]:
        new_node_of = {}

        def get_new_node_of(old_node):
            if old_node not in new_node_of:
                new_node_of[old_node] = deepcopy(old_node)

            return new_node_of[old_node]

        for old_node in nodes:
            new_node = get_new_node_of(old_node)
            self.add_node(new_node)

            for (port_name_old, port_old) in old_node.inputs.items():
                for connected_port in port_old.connections:

                    # Skip connecting if the node hasn't been visited
                    if connected_port.node not in new_node_of:
                        continue

                    new_connected_node = new_node_of[connected_port.node]

                    new_node.inputs[port_name_old].connect_to(
                        new_connected_node.outputs[connected_port.name]
                    )

            for (port_name_old, port_old) in old_node.outputs.items():
                for connected_port in port_old.connections:

                    # Skip connecting if the node hasn't been visited
                    if connected_port.node not in new_node_of:
                        continue

                    new_connected_node = new_node_of[connected_port.node]

                    new_node.outputs[port_name_old].connect_to(
                        new_connected_node.inputs[connected_port.name]
                    )

        return list(new_node_of.values())

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
