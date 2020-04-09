# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Dict, Type

import dependency_injector.providers as providers
from dial_core.node_editor import Node  # noqa: F401

from .node_transformer import NodeTransformer


class NodeTransformersRegistry:
    def __init__(self):
        super().__init__()

        self._registered_transformers: Dict["Node", "NodeTransformer"] = {}

    @property
    def transformers(self) -> Dict["Node", "NodeTransformer"]:
        """Returns a dictionary with all the registered transformers."""
        return self._registered_transformers

    def register_transformer(
        self, node_type: Type["Node"], transformer: "NodeTransformer"
    ):
        """Registers a new type of transformer.

        Args:
            node: Node class.
            transformer: Transformer for the class.
        """
        self._registered_transformers[node_type] = transformer

    def unregister_transformer(self, node_type: Type["Node"]):
        self._registered_transformers.pop(node_type, None)

    def clear(self):
        """Remove all registered transformers."""
        self._registered_transformers.clear()


NodeTransformersRegistrySingleton = providers.Singleton(NodeTransformersRegistry)
