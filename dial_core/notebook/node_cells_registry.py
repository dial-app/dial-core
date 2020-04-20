# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Dict, Type, Union

import dependency_injector.providers as providers

from .node_cells import NodeCells

if TYPE_CHECKING:
    from .dial_core.node_editor import Node


class NodeCellsRegistry:
    """The NodeCellsRegistry class provides a container for NodeCells
    associated to Node objects."""

    def __init__(self):
        self._registered_transformers: Dict[Type["Node"], Type["NodeCells"]] = {}

    @property
    def transformers(self) -> Dict[Type["Node"], Type["NodeCells"]]:
        """Returns a dictionary with all the registered transformers."""
        return self._registered_transformers

    def create_transformer_from(self, node: "Node", *args, **kwargs) -> "NodeCells":
        """Returns a NodeCells object created for the passed node instance.

        Raises:
            KeyError: If the type of `node` isn't registered and can't find a
            transformer.
        """
        return self._registered_transformers[node.__class__](node, *args, **kwargs)

    def register_transformer(
        self,
        node_type: Type["Node"],
        transformer: Union[Type["NodeCells"], providers.Factory],
        *args,
        **kwargs
    ):
        """Registers a new transformer for the `Node` objects.

        Args:
            node: Node class.
            transformer: NodeCells class or factory of NodeCells.
        """
        transformer_type = transformer

        if isinstance(transformer, providers.Factory):
            transformer_type = transformer.cls

        factory = providers.Factory(transformer_type, *args, **kwargs)

        self._registered_transformers[node_type] = factory

    def unregister_transformer(self, node_type: Type["Node"]):
        """Removes a registered transformer from the dictionary."""
        self._registered_transformers.pop(node_type, None)

    def clear(self):
        """Remove all registered transformers."""
        self._registered_transformers.clear()


NodeCellsRegistryFactory = providers.Factory(NodeCellsRegistry)
NodeCellsRegistrySingleton = providers.Singleton(NodeCellsRegistry)
