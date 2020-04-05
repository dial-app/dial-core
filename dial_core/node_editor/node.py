# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from dial_core.utils.exceptions import InvalidPortTypeError
from dial_core.utils.log import DEBUG, log_on_end

from .input_port import InputPort
from .output_port import OutputPort

if TYPE_CHECKING:
    from .port import Port


class Node:
    def __init__(self, title: str, inner_widget: Any = None):
        self._title = title

        self._inner_widget: Optional[Any] = inner_widget

        self._inputs: Dict[str, "InputPort"] = {}
        self._outputs: Dict[str, "OutputPort"] = {}

    @property
    def title(self) -> str:
        """Returns the title of the node."""
        return self._title

    @title.setter
    def title(self, title: str):
        """Sets a new title for the node.

        Emits:
            title_changed
        """
        self._title = title

    @property
    def inner_widget(self) -> Optional[Any]:
        """Returns the inner widget set on the node (Or None if not used)."""
        return self._inner_widget

    @property
    def inputs(self) -> Dict[str, "InputPort"]:
        """Returns a list of the input ports of the node."""
        return self._inputs

    @property
    def outputs(self) -> Dict[str, "OutputPort"]:
        """Returns a list of the output ports of the node."""
        return self._outputs

    def add_input_port(self, name: str, port_type: Any) -> "InputPort":
        """Creates a new input port and adds it to the list of ports.

        Args:
            name: Name of the port.
            port_type: Type of the port.

        Retuns:
            The added InputPort instance.
        """
        return self.__add_port_to(self.inputs, InputPort(name, port_type))

    def add_output_port(self, name: str, port_type: Any) -> "OutputPort":
        """Creates a new output port and adds it to the list of ports.

        Args:
            name: Name of the port.
            port_type: Type of the port.

        Retuns:
            The added InputPort instance.
        """
        return self.__add_port_to(self.outputs, OutputPort(name, port_type))

    def add_port(
        self, port: Union["InputPort", "OutputPort"]
    ) -> Union["InputPort", "OutputPort"]:
        """Adds a port instance to this node.

        Important:
            The port to add must be a child of `InputPort` or `OutputPort`. Otherwise,
            it won't be added and a `TypeError` exception will be raised.

        Retuns:
            The port instance added.

        Raises:
            TypeError: If the `port` argument passed is not a chid of `InputPort` or
            `OutputPort`
        """
        if isinstance(port, InputPort):
            return self.__add_port_to(self.inputs, port)
        elif isinstance(port, OutputPort):
            return self.__add_port_to(self.outputs, port)
        else:
            raise InvalidPortTypeError(
                "Port {port} must be of type InputPort or OutputPort."
            )

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
    def __add_port_to(self, ports_dict: Dict[str, "Port"], port: "Port") -> "Port":
        """Adds a port to a dictionary of ports.

        When a port is added, a reference to this Node is added (`port.node = self`)

        Args:
            ports_dict: Dictionary of all the ports.
            port: Port object to add.

        Returns:
            The added port instance.
        """
        ports_dict[port.name] = port
        port.node = self

        return port

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

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result

        setattr(result, "_title", deepcopy(self._title, memo))
        setattr(result, "_inputs", deepcopy(self._inputs, memo))
        setattr(result, "_outputs", deepcopy(self._outputs, memo))
        setattr(result, "_inner_widget", deepcopy(self._inner_widget, memo))

        for port in list(self.inputs.values()) + list(self.outputs.values()):
            port.node = self

        return result

    def __hash__(self):
        return hash(id(self))

    def __eq__(self, other):
        if isinstance(other, Node):
            return (
                self.inputs == other.inputs
                and self.outputs == other.outputs
                and self.title == other.title
                and self.inner_widget == other.inner_widget
            )

    def __getstate__(self):
        return {"inputs": self._inputs, "outputs": self._outputs}

    def __setstate__(self, new_state):
        self._inputs = new_state["inputs"]
        self._outputs = new_state["outputs"]

    def __reduce__(self):
        return (Node, (self._title, self._inner_widget), self.__getstate__())

    def __str__(self):
        """Retuns the string representation of the Port object."""
        return f'{type(self).__name__} "{self.title}" '

    def __repr__(self):
        """Returns the object representation of the Port object (with mem address)."""
        return (
            f'{type(self).__name__} "{self.title}"'
            f"({str(id(self))[:4]}...{str(id(self))[-4:]})"
        )
