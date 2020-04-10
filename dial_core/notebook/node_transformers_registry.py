# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Dict, Type, Union

import dependency_injector.providers as providers

from dial_core.node_editor import Node  # noqa: F401

from .node_transformer import NodeTransformer  # noqa: F401


class NodeTransformersRegistry:
    def __init__(self):
        super().__init__()

        self._registered_transformers: Dict[Type["Node"], Type["NodeTransformer"]] = {}

    @property
    def transformers(self) -> Dict[Type["Node"], Type["NodeTransformer"]]:
        """Returns a dictionary with all the registered transformers."""
        return self._registered_transformers

    def create_transformer_from(self, node, *args, **kwargs):
        return self._registered_transformers[node.__class__](node, *args, **kwargs)

    def register_transformer(
        self,
        node_type: Type["Node"],
        transformer: Union[Type["NodeTransformer"], providers.Factory],
        *args,
        **kwargs
    ):
        """Registers a new type of transformer.

        Args:
            node: Node class.
            transformer: Transformer for the class.
        """
        transformer_type = transformer

        if isinstance(transformer, providers.Factory):
            transformer_type = transformer.cls

        factory = providers.Factory(transformer_type, *args, **kwargs)

        self._registered_transformers[node_type] = factory

    def unregister_transformer(self, node_type: Type["Node"]):
        self._registered_transformers.pop(node_type, None)

    def clear(self):
        """Remove all registered transformers."""
        self._registered_transformers.clear()


NodeTransformersRegistrySingleton = providers.Singleton(NodeTransformersRegistry)
