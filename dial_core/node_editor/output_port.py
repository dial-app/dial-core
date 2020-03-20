# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Callable, Dict, Optional

from dial_core.utils.log import DEBUG, log_on_end

from .port import Port


class OutputPort(Port):
    def __init__(self, name: str, port_type: Any):
        super().__init__(name, port_type, allows_multiple_connections=True)

        from .input_port import InputPort
        self.compatible_port_classes.add(InputPort)

        self.output_generator: Optional[Callable] = None

    @log_on_end(
        DEBUG, '{self}: Value generated from "{self.output_generator.__name__}"'
    )
    def get_output_value(self):
        """Returns the value this port expects from the connected node.

        Raises:
            AttributeError: If the port doesn't have an output generator function
            attached.
        """
        if not self.output_generator:
            raise AttributeError("{self} doesn't has a generator function attached!")

        return self.output_generator()

    def propagate(self):
        """Starts processing each connected node."""
        for port in self.connections:
            port.node.process()

    def __getstate__(self) -> Dict[str, Any]:
        state = super().__getstate__()
        state["output_generator"] = self.output_generator

        return state

    def __setstate__(self, new_state: Dict[str, Any]):
        super().__setstate__(new_state)

        self.output_generator = new_state["output_generator"]

    def __reduce__(self):
        return (OutputPort, (self.name, self.port_type), self.__getstate__())
