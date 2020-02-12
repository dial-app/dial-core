# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Type

from .port import Port


class OutputPort(Port):
    def __init__(self, port_type: Type):
        super().__init__(port_type, allows_multiple_connections=False)

        self.processing_function = None

    def get_result(self):
        """Returns the value this port expects from the connected node."""
        return self.processing_function()
