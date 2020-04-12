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
    def __init__(self, name="Value Node", value=0):
        super().__init__(name)

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
            f'{self._node.outputs["value"].word_id()} = {self._node.value}'
        )

        return [value_cell]


class PrintNode(Node):
    def __init__(self, name="Print Node"):
        super().__init__(name)

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
            f"print({self._node.inputs['value'].word_id()})"
        )

        return [print_cell]


def test_generate_notebook():
    transformers_registry = NodeTransformersRegistry()
    transformers_registry.register_transformer(ValueNode, ValueNodeTransformer)
    transformers_registry.register_transformer(PrintNode, PrintNodeTransformer)

    project = DefaultProjectFactory()

    value_node_1 = ValueNode(name="Operator 1", value=1)
    print_node_1 = PrintNode(name="Printer 1")
    value_node_1.outputs["value"].connect_to(print_node_1.inputs["value"])

    value_node_2 = ValueNode(name="Operator 2", value=2)
    print_node_2 = PrintNode(name="Printer 2")
    value_node_2.outputs["value"].connect_to(print_node_2.inputs["value"])

    notebook_project_generator = NotebookProjectGeneratorFactory(
        node_transformers_registry=transformers_registry
    )

    project.scene.add_node(print_node_1)
    project.scene.add_node(print_node_2)
    project.scene.add_node(value_node_1)
    project.scene.add_node(value_node_2)

    project.scene.remove_node(print_node_1)
    project.scene.remove_node(value_node_1)

    print(notebook_project_generator.notebook.cells)

    notebook_project_generator.save_notebook_as("testnb.ipynb")
