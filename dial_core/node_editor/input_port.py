# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from copy import deepcopy
from typing import Any, Callable, Dict, Optional

from dial_core.utils import log
from dial_core.utils.exceptions import PortNotConnectedError

from .port import Port

LOGGER = log.get_logger(__name__)


class InputPort(Port):
    def __init__(self, name: str, port_type: Any):
        super().__init__(name, port_type, allows_multiple_connections=False)

        from .output_port import OutputPort

        self.compatible_port_classes.add(OutputPort)

        self._is_receiving_input = True
        self._processor_function: Optional[Callable] = None

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

    def toggle_receives_input(self, toggle: bool):
        self._is_receiving_input = toggle

    def set_processor_function(self, processor_function: Callable):
        self._processor_function = processor_function

    def process_input(self, value: Any):
        if not self._is_receiving_input:
            return

        if not self._processor_function:
            raise NotImplementedError(f"`processor_function` not implemented in {self}")

        try:
            self._processor_function(value)
        except PortNotConnectedError as err:
            LOGGER.debug(
                "%s processor function failed (%s) Details:\n%s",
                self,
                self._processor_function.__name__,
                str(err),
            )

    def receive(self) -> Any:
        if not self.port_connected_to:
            raise PortNotConnectedError(f"{self} is not connected to any other port.")

        return self.port_connected_to.generate_output()

    def propagate_to(self, output_port):
        def processor_function_propagate_to(self):
            output_port.send()

        self._processor_function = processor_function_propagate_to

    def __deepcopy__(self, memo):
        base = super().__deepcopy__(memo)

        setattr(base, "_is_receiving_input", deepcopy(self._is_receiving_input, memo))
        setattr(base, "_processor_function", deepcopy(self._processor_function, memo))

        return base

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()
        state["processor_function"] = self._processor_function

        return state

    def __setstate__(self, new_state: Dict[str, Any]):
        super().__setstate__(new_state)

        self._processor_function = new_state["processor_function"]

    def __reduce__(self):
        return (InputPort, (self.name, self.port_type), self.__getstate__())
