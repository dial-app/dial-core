# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Optional, Set

from dial_core.utils.log import DEBUG, ERROR, log_on_end, log_on_error


class Port:
    def __init__(
        self, name: str, port_type: Any, allows_multiple_connections: bool = True
    ):
        self.__name = name
        self.__port_type = port_type
        self.__connected_to: Set["Port"] = set()  # Avoid repeat ports

        self.node: Optional["Node"] = None  # type: ignore

        self.allows_multiple_connections = allows_multiple_connections

    @property
    def name(self) -> str:
        """Returns the name (identifier) of the port."""
        return self.__name

    @property
    def port_type(self) -> Any:
        """Returns the Type allowed by this port.

        Used to check which ports can be connected between them.
        """
        return self.__port_type

    @property
    def connections(self) -> Set["Port"]:
        """Returns the ports this port is currently connected.

        Shouldn't be manipulated directly. Use the `connect_to`, `disconnect_from`
        functions to handle port connections

        Returns:
           A set with all the Ports connected to this port.
        """
        return self.__connected_to

    def is_compatible_with(self, port: "Port") -> bool:
        """Checks if this port is compatible with another port.

        Two ports are compatible if they're of the same type and don't belong to the
        same node.

        Args:
            port: Port being compared with.
        """
        return self.__port_type == port.port_type and (
            not self.node or self.node != port.node
        )

    @log_on_end(DEBUG, "{self} connected to {port}")
    @log_on_error(
        ERROR, "Error on connection: {e}", on_exceptions=(ValueError), reraise=True
    )
    def connect_to(self, port: "Port"):
        """Connects the current port to another port.

        Its a two way connection (the two ports will be connected to each other)
        a = Port()
        b = Port()
        a.connect_to(b)

        Args:
            port: `Port` object being connected to.

        Raises:
            ValueError: If the port is connected to itself.
            ValueError: If the ports aren't compatible (can't be connected).
        """
        if port is self:  # Avoid connecting a port to itself
            raise ValueError(f"Can't connect {port} to itself!")

        if not self.is_compatible_with(port):
            raise ValueError(
                f"This port ({self}) type is not compatible with the"
                f" other port. ({port})"
            )

        if not self.allows_multiple_connections:
            # Disconnect from other ports before setting the new connection
            self.clear_all_connections()

        # Two way connection (Both ports will have a reference to each other)
        self.__connected_to.add(port)
        if self not in port.connections:
            port.connect_to(self)

    @log_on_end(DEBUG, "Port {self} disconnected from {port}")
    def disconnect_from(self, port: "Port"):
        """Disconnects the current port from the other port.

        Args:
            port: `Port` object being disconnect from.
        """
        if port not in self.__connected_to:  # Can't remove port if not found
            return

        # Two way disconnection
        self.__connected_to.discard(port)
        port.disconnect_from(self)

    @log_on_end(DEBUG, "All connections cleared on {self}")
    def clear_all_connections(self):
        """Removes all connections to this port."""

        # Use a list to avoid removing an item from self.__connected_to while iterating
        for port in list(self.__connected_to):
            port.disconnect_from(self)

        self.__connected_to.clear()

    def __str__(self):
        """Retuns the string representation of the Port object."""
        return f'{type(self).__name__} "{self.name}" [{self.port_type.__str__}]'

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        return (
            f'{type(self).__name__} "{self.name}"'
            f" ({str(id(self))[:4]}...{str(id(self))[-4:]})"
            f" [{self.port_type.__str__}] from {self.node}"
        )
