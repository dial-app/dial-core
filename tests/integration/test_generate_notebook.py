import nbformat as nbf

from dial_core.node_editor import Node
from dial_core.notebook import (
    NodeCells,
    NodeCellsRegistry,
    NotebookProjectGeneratorFactory,
)
from dial_core.project import DefaultProjectFactory


class ValueNode(Node):
    def __init__(self, name="Value Node", value=0):
        super().__init__(name)

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
    def _body_cells(self):
        value_cell = nbf.v4.new_code_cell(
            f'{self._node.outputs["value"].word_id()} = {self._node.value}'
        )

        return [value_cell]


class PrintNode(Node):
    def __init__(self, name="Print Node"):
        super().__init__(name)

        self.add_input_port(name="value", port_type=int)
        self.inputs["value"].set_processor_function(self._print_value)

    def print_input(self):
        value = self.inputs["value"].receive()
        self._print_value(value)

    def _print_value(self, value):
        print(value)


class PrintNodeCells(NodeCells):
    def _body_cells(self):
        print_cell = nbf.v4.new_code_cell(
            f"print({self._node.inputs['value'].word_id()})"
        )

        return [print_cell]


def test_generate_notebook():
    transformers_registry = NodeCellsRegistry()
    transformers_registry.register_transformer(ValueNode, ValueNodeCells)
    transformers_registry.register_transformer(PrintNode, PrintNodeCells)

    project = DefaultProjectFactory()

    value_node_1 = ValueNode(name="Operator 1", value=1)
    print_node_1 = PrintNode(name="Printer 1")
    value_node_1.outputs["value"].connect_to(print_node_1.inputs["value"])

    value_node_2 = ValueNode(name="Operator 2", value=2)
    print_node_2 = PrintNode(name="Printer 2")
    value_node_2.outputs["value"].connect_to(print_node_2.inputs["value"])

    notebook_project_generator = NotebookProjectGeneratorFactory(
        node_cells_registry=transformers_registry
    )

    project.scene.add_node(print_node_1)
    project.scene.add_node(print_node_2)
    project.scene.add_node(value_node_1)
    project.scene.add_node(value_node_2)

    project.scene.remove_node(print_node_1)
    project.scene.remove_node(value_node_1)

    notebook_project_generator.set_project(project)
    print(notebook_project_generator.notebook.cells)

    # notebook_project_generator.save_notebook_as("testnb.ipynb")
