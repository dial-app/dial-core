# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf

from dial_core.node_editor import Node
from dial_core.notebook import NodeCells


class ValueNode(Node):
    def __init__(self, value=0):
        super().__init__("Value Node")

        # Port configuration
        self.add_output_port(name="value", port_type=int)
        self.outputs["value"].set_generator_function(self.__generate_value)

        # Attributes
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

        self.outputs["value"].send()

    def __generate_value(self):
        return self.value


class ValueNodeCells(NodeCells):
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            f'{self.node.outputs["value"].word_id()} = {self._node.value}'
        )

        return [value_cell]


def test_value_node_cells():
    value_node = ValueNode(value=8)

    value_node_transformer = ValueNodeCells(value_node)

    cells = value_node_transformer.cells()

    assert cells[0].cell_type == "markdown"
    assert cells[0].source == "## Value Node (ValueNode)"

    assert cells[1].cell_type == "code"
    assert cells[1].source == (
        f'{value_node_transformer.node.outputs["value"].word_id()}'
        f" = {value_node.value}"
    )
