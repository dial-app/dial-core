# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Callable, Dict, Optional

from .port import Port

# from dial_core.utils.log import DEBUG, log_on_end


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
        except (NotImplementedError, ValueError):
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

        try:
            value = self.generate_output()

            for input_port in self.connections:
                # if port.receive_propagated_values:
                input_port.process_input(value)

        except ValueError:  # Error in generate_output, can't propagate
            pass

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()
        state["generator_function"] = self._generator_function

        return state

    def __setstate__(self, new_state: Dict[str, Any]):
        super().__setstate__(new_state)

        self._generator_function = new_state["generator_function"]

    def __reduce__(self):
        return (OutputPort, (self.name, self.port_type), self.__getstate__())
