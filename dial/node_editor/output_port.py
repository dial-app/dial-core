# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Type

from .port import Port


class OutputPort(Port):
    def __init__(self, port_type: Type):
        super().__init__(port_type, allows_multiple_connections=True)

        self.function_to_generate_output = None

    def get_output_value(self):
        """Returns the value this port expects from the connected node."""
        if not self.function_to_generate_output:
            raise NotImplementedError(
                "Output Port {self} doesn't has an implementation!"
            )

        return self.function_to_generate_output()

    def send(self):
        for port in self.connections:
            port.node.process()
