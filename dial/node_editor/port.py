# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Can:
  * Connect/Discconnect to another port.
  * Detect and prevent being connected to itself.
  * Connect to several ports or only one port at a time.
  * Check if two ports are compatible and can be connected
"""

from typing import Set, Type


class Port:
    def __init__(self, port_type: Type, allows_multiple_connections: bool = True):
        self.__port_type = port_type
        self.__connected_to: Set["Port"] = set()  # Avoid repeat ports

        self.process_func = None

        self.allows_multiple_connections = allows_multiple_connections

    @property
    def port_type(self) -> Type:
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

        Args:
            port: Port being compared with.
        """
        return self.__port_type == port.port_type

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
            raise ValueError(f"Can't connect port {port} to itself!")

        if port in self.__connected_to:  # The ports are already connected
            return

        if not self.is_compatible_with(port):
            raise ValueError(
                f"This port ({self.port_type}) isn't compatible with the"
                f"other port! ({port.port_type})"
            )

        if not self.allows_multiple_connections:
            # Disconnect from other ports before setting the new connection
            for connected_port in list(self.__connected_to):
                connected_port.disconnect_from(self)

        # Two way connection (Both ports will have a reference to each other)
        self.__connected_to.add(port)
        port.connect_to(self)

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

    def clear_all_connections(self):
        """Remove all connections to this port."""

        # Use a list to avoid a port while iterating the list
        for port in list(self.__connected_to):
            port.disconnect_from(self)

        self.__connected_to.clear()
