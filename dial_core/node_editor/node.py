# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Dict, Optional

from dial_core.utils.log import DEBUG, log_on_end

if TYPE_CHECKING:
    from .input_port import InputPort
    from .output_port import OutputPort
    from .port import Port


class Node:
    def __init__(self, title: str, inner_widget: Any = None):
        self.__title = title

        self.__inner_widget: Optional[Any] = inner_widget

        self.__inputs: Dict[str, "InputPort"] = {}
        self.__outputs: Dict[str, "OutputPort"] = {}

    @property
    def title(self) -> str:
        """Returns the title of the node."""
        return self.__title

    @title.setter
    def title(self, title: str):
        """Sets a new title for the node. Emits the `title_changed` signal.

        Emits:
            title_changed
        """
        self.__title = title

    @property
    def inner_widget(self) -> Optional[Any]:
        """Returns the inner widget set on the node (Or None if not used)."""
        return self.__inner_widget

    @property
    def inputs(self) -> Dict[str, "InputPort"]:
        """Returns a list of the input ports of the node."""
        return self.__inputs

    @property
    def outputs(self) -> Dict[str, "OutputPort"]:
        """Returns a list of the output ports of the node."""
        return self.__outputs

    def process(self):
        """Sends the output of each port to the connected nodes."""
        for output_port in self.outputs.values():
            output_port.propagate()

    def add_input_port(self, input_port: "InputPort"):
        """Adds a new input port to the list of ports.

        Args:
            input_port: Port object added to the input ports list.
        """
        self.__add_port_to(self.inputs, input_port)

    def add_output_port(self, output_port: "OutputPort"):
        """Adds a new output port to the list of ports.

        Args:
            output_port: Port object added to the output ports list.
        """
        self.__add_port_to(self.outputs, output_port)

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

    @log_on_end(DEBUG, "{port} added to {self}")
    def __add_port_to(self, ports_dict: Dict[str, "Port"], port: "Port"):
        """Adds a port to a dictionary of ports.

        When a port is added, a reference to this Node is added (`port.node = self`)

        Args:
            ports_dict: Dictionary of all the ports.
            port: Port object to add.
        """
        ports_dict[port.name] = port
        port.node = self

    @log_on_end(DEBUG, "{port_name} removed from {self}")
    def __remove_port_from(self, ports_dict: Dict[str, "Port"], port_name: str) -> bool:
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
        return f'{type(self).__name__} "{self.title}" '

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        return (
            f'{type(self).__name__} "{self.title}"'
            f"({str(id(self))[:4]}...{str(id(self))[-4:]})"
        )
