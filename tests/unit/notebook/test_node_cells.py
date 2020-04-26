# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf

from dial_core.node_editor import Node
from dial_core.notebook import NodeCells


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_input_port(name="test", port_type=int)
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
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            f'{self.node.outputs["value"].word_id()} = {self.node.value}'
        )

        return [value_cell]


def test_value_node_cells():
    value_node = ValueNode(value=8)

    value_node_transformer = ValueNodeCells(value_node)

    cells = value_node_transformer.cells()

    assert cells[0].cell_type == "markdown"
    assert cells[0].source == "## Value Node (ValueNode)"

    assert cells[1].cell_type == "code"
    assert cells[2].source == (
        f'{value_node_transformer.node.outputs["value"].word_id()}'
        f" = {value_node.value}"
    )


def test_input_variable_cells():
    value_node = ValueNode(value=8)

    value_node_transformer = ValueNodeCells(value_node)

    input_cells = value_node_transformer._input_variables_cells()

    assert input_cells[0].source == (
        f"# Input variables\n{value_node.inputs['test'].word_id()} = None\n"
    )
