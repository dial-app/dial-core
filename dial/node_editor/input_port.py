# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional, Type

from .port import Port


class InputPort(Port):
    def __init__(self, port_type: Type):
        super().__init__(port_type, allows_multiple_connections=False)

    @property
    def port_connected_to(self) -> Optional[Port]:
        """Returns the port connected to this one (can be None).

        Because this is an Input Port, we can ensure it can be connected to only one (1)
        another port.

        Returns:
            The port its connected to (or None if no port connected)
        """
        if self.connections:
            return list(self.connections)[0]

        return None

    def receive(self):
        return self.port_connected_to.get_result()
