# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Optional, Set, Type

from dial_core.utils.log import DEBUG, ERROR, log_on_end, log_on_error


class Port:
    """The Port class provides a connection point between different nodes.

    A Port object allows two types of connections:
        * one-to-one: This Port can be only connected to another port.
        * many-to-many: This Port can be connected to multiple ports, and multiple ports
            can be connected to this one.

    A Port object also has an associated Type. Two Port objects can only be connected if
    they share the same Type.

    Attributes:
        name: The name (identifier) of the port. Can't be changed once the Port is
            created.
        port_type: The type of this port. A Port object can only be connected to other
            Ports that share its same type.
        connections: Set with all the Ports this port is currently connected to.
        node: The Node object this Port belongs to, if any.
        allows_multiple_connections: A boolean option, indicating the type of connection
        this port allows (one-to-one or many-to-many)
    """

    def __init__(
        self, name: str, port_type: Any, allows_multiple_connections: bool = True
    ):
        self.__name = name
        self.__port_type = port_type
        self.__connected_to: Set["Port"] = set()  # Avoid repeat ports
        self.compatible_port_classes: Set[Type["Port"]] = set([Port])

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
        return (
            self.__port_type == port.port_type
            and (not self.node or self.node != port.node)
            and type(port) in self.compatible_port_classes
        )

    @log_on_end(DEBUG, "{self} connected to {port}")
    @log_on_error(ERROR, "Error on connection: {e}", on_exceptions=(ValueError))
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

    def __getstate__(self):
        return {"connected_to": self.__connected_to, "node": self.node}

    def __setstate__(self, new_state):
        self.__connected_to = new_state["connected_to"]
        self.node = new_state["node"]

    def __reduce__(self):
        return (
            Port,
            (self.name, self.port_type, self.allows_multiple_connections),
            self.__getstate__(),
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.name == other.name
            and self.port_type == other.port_type
            and self.allows_multiple_connections == other.allows_multiple_connections
        )

    def __hash__(self):
        return hash((self.name, self.port_type, self.allows_multiple_connections))

    def __str__(self):
        """Retuns the string representation of the Port object."""
        type_str = (
            self.port_type.__name__
            if isinstance(self.port_type, type)
            else self.port_type
        )
        return f'{self.__class__.__name__} "{self.name}" [{type_str}]'

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        type_str = (
            self.port_type.__name__
            if isinstance(self.port_type, type)
            else self.port_type
        )
        return (
            f'{self.__class__.__name__} "{self.name}"'
            f" ({str(id(self))[:4]}...{str(id(self))[-4:]})"
            f" [{type_str}] from {self.node}"
        )
