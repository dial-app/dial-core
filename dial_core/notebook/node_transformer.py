# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


import nbformat as nbf


class NodeTransformer:
    def __init__(self, node):
        self._node = node

    def cells(self):
        return self._header_cells() + self._input_variables() + self._body_cells()

    def _title_cells(self):
        return [
            nbf.v4.new_markdown_cell(
                source=f"## {self._node.title} ({type(self._node).__name__})"
            )
        ]

    def _header_cells(self):
        """Returns Title and Description cells, for example."""
        return self._title_cells()

    def _input_variables(self):
        if len(self._node.inputs) == 0:
            return []

        input_variables_code = "# Input variables\n"

        for input_port in self._node.inputs.values():
            if input_port.port_connected_to is not None:
                connected_variable_name = input_port.port_connected_to.word_id()
                input_variables_code += (
                    f"{input_port.word_id()} = {connected_variable_name}"
                )

        return [nbf.v4.new_code_cell(source=input_variables_code)]

    def _body_cells(self):
        """Returns Code and Explanations cells, for example."""
        return []

    def _as_variable_name(self, string: str) -> str:
        return string.lower().replace(" ", "_")
