# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Optional

from dial_core.utils.log import DEBUG, log_on_end

from .port import Port


class InputPort(Port):
    def __init__(self, name: str, port_type: Any):
        super().__init__(name, port_type, allows_multiple_connections=False)

        from .output_port import OutputPort

        self.compatible_port_classes.add(OutputPort)

    @property
    def port_connected_to(self) -> Optional["Port"]:
        """Returns the port connected to this one (can be None).

        Because this is an Input Port, we can ensure it can be connected to only one (1)
        another port.

        Returns:
            The port its connected to (or None if no port connected)
        """
        if self.connections:
            return list(self.connections)[0]

        return None

    @log_on_end(DEBUG, "{self}: Value received")
    def receive(self):
        """Gets the output value of the connected OutputPort."""
        return self.port_connected_to.get_output_value()

    def __getstate__(self):
        return super().__getstate__()

    def __reduce__(self):
        return (InputPort, (self.name, self.port_type), self.__getstate__())
