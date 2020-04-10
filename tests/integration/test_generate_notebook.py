import nbformat as nbf
import pytest

from dial_core.node_editor import Node
from dial_core.notebook import (
    NodeTransformer,
    NodeTransformersRegistry,
    NotebookProjectGeneratorFactory,
)
from dial_core.project import DefaultProjectFactory


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


class ValueNodeTransformer(NodeTransformer):
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            f'{self._node.outputs["value"]._variable_name} = {self._node.value}'
        )

        return [value_cell]


class PrintNode(Node):
    def __init__(self):
        super().__init__("Print Node")

        self.add_input_port(name="value", port_type=int)
        self.inputs["value"].set_processor_function(self.__print_value)

    def print_input(self):
        value = self.inputs["value"].receive()
        self.__print_value(value)

    def __print_value(self, value):
        print(value)


class PrintNodeTransformer(NodeTransformer):
    def _body_cells(self):
        print_cell = nbf.v4.new_code_cell(
            f"print({self._node.inputs['value']._variable_name})"
        )

        return [print_cell]


def test_generate_notebook():
    transformers_registry = NodeTransformersRegistry()
    transformers_registry.register_transformer(ValueNode, ValueNodeTransformer)
    transformers_registry.register_transformer(PrintNode, PrintNodeTransformer)

    project = DefaultProjectFactory()

    value_node = ValueNode(value=8)
    print_node = PrintNode()
    value_node.outputs["value"].connect_to(print_node.inputs["value"])

    project.scene.add_node(value_node)
    project.scene.add_node(print_node)

    notebook_project_generator = NotebookProjectGeneratorFactory(
        project=project, node_transformers_registry=transformers_registry
    )

    print(notebook_project_generator.notebook.cells)

    notebook_project_generator.save_notebook_as("testnb.ipynb")

    pytest.fail("Catch")
