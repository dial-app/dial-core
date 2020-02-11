# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Dict

from .port import Port


"""
Can:
 * Connect and disconnect from/to different nodes
 * Add/remove new ports as input/output ports
"""


class Node:
    def __init__(self, title):
        self.title = title

        self.__inputs = {}
        self.__outputs = {}

    @property
    def inputs(self):
        """Returns a list of the input ports of the node."""
        return self.__inputs

    @property
    def outputs(self):
        """Returns a list of the output ports of the node."""
        return self.__outputs

    def add_input(self, port_name, input_port):
        """Adds a new input port to the list of ports.

        Args:
            port_name: Name of the port being added.
            input_port: Port object added to the input ports list.
    """
        self.inputs[port_name] = input_port

    def add_output(self, port_name, output_port):
        """Adds a new output port to the list of ports.

        Args:
            port_name: Name of the port being added.
            output_port: Port object added to the output ports list.
        """
        self.outputs[port_name] = output_port

    def remove_input(self, port_name: str):
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

    def remove_output(self, port_name: str):
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

    def __remove_port_from(self, ports_dict: Dict[str, Port], port_name: str) -> bool:
        """Remove a port from a dictionary of ports.

        Before removing, if the ports is present, it is disconnected from all other
        ports to prevent having ports with hanging connections.
        """
        if port_name not in ports_dict:
            return False

        # Disconnect this port from all other connected ports before removing. This will
        # preveing having a port with hanging connections to deleted ports.
        ports_dict[port_name].clear_all_connections()
        del ports_dict[port_name]

        return True
