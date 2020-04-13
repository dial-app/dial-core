# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Dict, List

import nbformat as nbf

if TYPE_CHECKING:
    from dial_core.node_editor import Node


class NodeCells:
    """The NodeCells class is the base implementation for a transformation between Node
    instances and cells that can be inserted on a Jupyter notebook.

    Attributes:
        node: The associated Node instance.
    """

    def __init__(self, node: "Node"):
        self._node = node

    @property
    def node(self) -> "Node":
        """Returns the Node instance related to this transformer."""
        return self._node

    def cells(self) -> List[Dict[str, str]]:
        """Returns the cells that form this node."""
        return self._header_cells() + self._input_variables_cells() + self._body_cells()

    def _title_cells(self) -> List[Dict[str, str]]:
        """Returns the cells corresponding to the title.

        By default, returns a header with the name and node type.
        """
        return [
            nbf.v4.new_markdown_cell(
                source=f"## {self._node.title} ({type(self._node).__name__})"
            )
        ]

    def _header_cells(self) -> List[Dict[str, str]]:
        """Returns the title cells."""
        return self._title_cells()

    def _input_variables_cells(self):
        """Returns the cells that define the input variables used by this node."""
        if len(self._node.inputs) == 0:
            return []

        input_variables_code = "# Input variables\n"

        for input_port in self._node.inputs.values():
            connected_variable_name = (
                input_port.port_connected_to.word_id()
                if input_port.port_connected_to
                else "None"
            )
            input_variables_code += (
                f"{input_port.word_id()} = {connected_variable_name}\n"
            )

        return [nbf.v4.new_code_cell(source=input_variables_code)]

    def _body_cells(self):
        """Returns Code and Explanations cells, for example.

        Must be implemented on subclasses.
        """
        return []
