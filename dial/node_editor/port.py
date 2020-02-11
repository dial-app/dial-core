# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


class Port:
    def __init__(self, allows_multiple_connections=True):
        self.__connected_to = set()  # Avoid repeat ports

        self.allows_multiple_connections = allows_multiple_connections

    @property
    def connections(self):
        """Returns the ports this port is currently connected.

        Shouldn't be manipulated directly. Use the `connect_to`, `disconnect_from`
        functions to handle port connections
        """
        return self.__connected_to

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
        """
        if port is self:  # Avoid connecting a port to itself
            raise ValueError("Can't connect port {port} to itself!")

        if port in self.__connected_to:  # The ports are already connected
            return

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

        for port in self.__connected_to:
            port.disconnect_from(self)

        self.__connected_to.clear()
