# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.node_editor import Node
from dial_core.notebook import NodeCells


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(name="value", port_type=int)
        self.outputs["value"].set_generator_function(self._generate_value)

        # Attributes
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

        self.outputs["value"].send()

    def _generate_value(self):
        return self.value


class ValueNodeCells(NodeCells):
    def transform(self):
        pass


def test_register_transformer(node_transformers_registry):
    node_transformers_registry.register_transformer(ValueNode, ValueNodeCells)

    assert ValueNode in node_transformers_registry.transformers

    value_node = ValueNode(value=7)

    # Test that doesn't raise
    node_transformers_registry.create_transformer_from(value_node)


def test_create_unregistered_transformer(node_transformers_registry):
    with pytest.raises(KeyError):
        node_transformers_registry.create_transformer_from(int)


def test_unregister_transformer(node_transformers_registry):
    node_transformers_registry.register_transformer(ValueNode, ValueNodeCells)

    node_transformers_registry.unregister_transformer(ValueNode)

    assert ValueNode not in node_transformers_registry.transformers


def test_clear_transformers(node_transformers_registry):
    node_transformers_registry.register_transformer(ValueNode, ValueNodeCells)

    node_transformers_registry.clear()

    assert len(node_transformers_registry.transformers) == 0
