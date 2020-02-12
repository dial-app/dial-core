# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Can:
 * Connect and disconnect from/to different nodes
 * Add/remove new ports as input/output ports
"""

from logging import DEBUG
from typing import Dict

from logdecorator import log_on_end

from .port import Port


class Node:
    def __init__(self, title: str):
        self.title = title

        self.__inputs: Dict[str, Port] = {}
        self.__outputs: Dict[str, Port] = {}

    @property
    def inputs(self) -> Dict[str, Port]:
        """Returns a list of the input ports of the node."""
        return self.__inputs

    @property
    def outputs(self) -> Dict[str, Port]:
        """Returns a list of the output ports of the node."""
        return self.__outputs

    def process(self):
        for output_port in self.outputs.values():
            output_port.propagate()

    def add_input_port(self, port_name: str, input_port: Port):
        """Adds a new input port to the list of ports.

        Args:
            port_name: Name of the port being added.
            input_port: Port object added to the input ports list.
        """
        self.__add_port_to(self.inputs, port_name, input_port)

    def add_output_port(self, port_name: str, output_port: Port):
        """Adds a new output port to the list of ports.

        Args:
            port_name: Name of the port being added.
            output_port: Port object added to the output ports list.
        """
        self.__add_port_to(self.outputs, port_name, output_port)

    def remove_input_port(self, port_name: str):
        """Removes an input port from the list of input ports.

        Args:
            port_name: Name of the port being removed.

        Raises:
            ValueError: If can't find a port to remove named `port_name`.
        """
        removed = self.__remove_port_from(self.inputs, port_name)

        if not removed:
            raise ValueError(
                f"Couldn't remove {port_name} from {self}! Missing port name from input"
            )

    def remove_output_port(self, port_name: str):
        """Removes an output port from the list of output ports.

        Args:
            port_name: Name of the port being removed.

        Raises:
            ValueError: If can't find a port to remove named `port_name`.
        """
        removed = self.__remove_port_from(self.outputs, port_name)

        if not removed:
            raise ValueError(
                f"Couldn't remove {port_name} from {self}! Missing port name from input"
            )

    @log_on_end(DEBUG, "{port!r} added to {self!r}")
    def __add_port_to(self, ports_dict: Dict[str, Port], port_name: str, port: Port):
        """Adds a port to a dictionary of ports.

        When a port is added, a reference to this Node is added (`port.node = self`)

        Args:
            ports_dict: Dictionary of all the ports.
            port_name: New name (identifier) for the port.
            port: Port object to add.
        """
        ports_dict[port_name] = port
        port.node = self

    @log_on_end(DEBUG, "{port!r} removed from {self!r}")
    def __remove_port_from(self, ports_dict: Dict[str, Port], port_name: str) -> bool:
        """Removes a port from a dictionary of ports.

        Before removing, if the ports is present, it is disconnected from all other
        ports to prevent having ports with hanging connections.

        Args:
            ports_dict: Dictionary of all the ports.
            port_name: Name (identifier) of the port.

        Returns:
            If the port was removed or not.
        """
        if port_name not in ports_dict:
            return False

        # Disconnect this port from all other connected ports before removing. This will
        # preveing having a port with hanging connections to deleted ports.
        ports_dict[port_name].clear_all_connections()
        ports_dict[port_name].node = None

        del ports_dict[port_name]

        return True

    def __str__(self):
        """Retuns the string representation of the Port object."""
        return f"{type(self).__name__}"

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        return f"{type(self).__name__}({str(id(self))[:4]}...{str(id(self))[-4:]})"
