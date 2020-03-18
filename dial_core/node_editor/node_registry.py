# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Dict, Type, Union

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .node import Node


class NodeRegistry(containers.DynamicContainer):
    def __init__(self):
        super().__init__()

    @property
    def nodes(self) -> Dict[str, "Node"]:
        """Returns a dictionary with all the registered nodes."""
        return self.providers

    def register_node(
        self,
        identifier: str,
        value: Union[Type["Node"], providers.Factory],
        *args,
        **kwargs
    ):
        """Registers a new type of node.

        Args:
            identifier: Name of the node.
            node_type: Node type.
        """

        node_type = value

        if isinstance(value, providers.Factory):
            node_type = value.cls  # Get Type produced by Factory

        if not issubclass(node_type, Node):
            raise TypeError("Registered nodes must inherit from `Node` class!!")

        factory = providers.Factory(value, *args, **kwargs)
        self.__register_factory(identifier, factory)

    def unregister_node(self, identifier: str):
        self.providers.pop(identifier, None)

    def __register_factory(self, identifier: str, node_factory: "providers.Factory"):
        """Registers a new node factory."""
        self.providers[identifier] = node_factory

    def get_node(self, identifier: str) -> "Node":
        """Returns an instanced node"""
        return self.providers[identifier]()

    def clear(self):
        """Removes all registered nodes."""
        self.providers.clear()


NodeRegistrySingleton = providers.Singleton(NodeRegistry)
