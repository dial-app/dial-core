# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


import nbformat as nbf


class NodeTransformer:
    def __init__(self, node):
        self._node = node

        self.input_variables = {}
        for input_port in self._node.inputs.keys():
            self.input_variables[input_port] = f"{input_port}"

        self.output_variables = {}
        for output_port in self._node.outputs.keys():
            self.output_variables[output_port] = f"{output_port}"

    def _title_cells(self):
        return [nbf.v4.new_markdown_cell(source=f"## {self._node.title}")]

    def _header_cells(self):
        """Returns Title and Description cells, for example."""
        return self._title_cells()

    def _body_cells(self):
        """Returns Code and Explanations cells, for example."""
        return []

    def cells(self):
        return self._header_cells() + self._body_cells()
