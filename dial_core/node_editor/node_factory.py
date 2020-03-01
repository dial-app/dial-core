# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Type

import dependency_injector.containers as containers
import dependency_injector.providers as providers

if TYPE_CHECKING:
    from .node import Node


class NodeFactory(containers.DynamicContainer):
    def __init__(self):
        super().__init__()

    @property
    def nodes(self):
        return self.providers

    def register_node(self, identifier: str, node_type: Type["Node"], *args, **kwargs):
        """Registers a new type of node.

        Args:
            identifier: Name of the node.
            node_type: Node type.
        """
        if not node_type:
            return

        factory = providers.Factory(node_type, *args, **kwargs)
        self.register_node_factory(identifier, factory)

    def register_node_factory(self, identifier: str, node_factory: "providers.Factory"):
        """Registers a new node factory."""
        if not node_factory:
            return

        self.providers[identifier] = node_factory

    def get_node(self, identifier: str) -> "Node":
        """Returns an instanced node"""
        return self.providers[identifier]()

    def clear(self):
        """Removes all registered nodes."""
        self.providers.clear()


NodeFactorySingleton = providers.Singleton(NodeFactory)
