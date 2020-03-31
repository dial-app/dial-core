# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Callable, Dict, Optional

# from dial_core.utils.log import DEBUG, log_on_end
from dial_core.utils.exceptions import PortNotConnectedError

from .port import Port


class OutputPort(Port):
    def __init__(self, name: str, port_type: Any):
        super().__init__(name, port_type, allows_multiple_connections=True)

        from .input_port import InputPort

        self.compatible_port_classes.add(InputPort)

        self.__is_sending_output = True
        self._generator_function: Optional[Callable] = None

    def toggle_sends_output(self, toggle: bool):
        self.__is_sending_output = toggle

    def connect_to(self, input_port):
        super().connect_to(input_port)

        try:
            input_port.process_input(self.generate_output())
        except (NotImplementedError, PortNotConnectedError):
            pass

    def set_generator_function(self, generator_function: Callable):
        self._generator_function = generator_function

    def generate_output(self):
        if not self._generator_function:
            raise NotImplementedError(f"`generator_function` not implemented in {self}")

        return self._generator_function()

    def send(self) -> Any:
        if not self.__is_sending_output:
            return

        # Sometimes, the generate_output() may need the value of connected InputPort.
        # If the function tries to access the value (calling `receive()`) but the
        # InputPort is not connected, the PortNotConnectedError exception is raised,
        # and no values are propagated to next ports
        try:
            value = self.generate_output()
        except PortNotConnectedError:
            return

        for input_port in self.connections:
            input_port.process_input(value)

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()
        state["generator_function"] = self._generator_function

        return state

    def __setstate__(self, new_state: Dict[str, Any]):
        super().__setstate__(new_state)

        self._generator_function = new_state["generator_function"]

    def __reduce__(self):
        return (OutputPort, (self.name, self.port_type), self.__getstate__())
