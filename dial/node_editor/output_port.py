# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from logging import DEBUG
from typing import Type

from logdecorator import log_on_end

from .port import Port


class OutputPort(Port):
    def __init__(self, name: str, port_type: Type):
        super().__init__(name, port_type, allows_multiple_connections=True)

        self.output_generator = None
        self._cached_output = None

    @log_on_end(
        DEBUG, '{self}: Value generated from "{self.output_generator.__name__}"'
    )
    def get_output_value(self):
        """Returns the value this port expects from the connected node."""
        if not self.output_generator:
            raise NotImplementedError(
                "Output Port {self} doesn't has an implementation!"
            )

        if not self._cached_output:
            self._cached_output = self.output_generator()

        return self._cached_output

    def propagate(self):
        for port in self.connections:
            port.node.process()
