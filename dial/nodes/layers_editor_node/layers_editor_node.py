# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import Dataset
from dial.node_editor import InputPort, Node, OutputPort

from .layers_editor_widget import LayersEditorWidget


class LayersEditorNode(Node):
    def __init__(self, parent=None):
        super().__init__(
            title="Layers Editor Node",
            inner_widget=LayersEditorWidget(),
            parent=parent,
        )

        print(self.inner_widget)

        # Ports
        self.add_input_port(InputPort("test", port_type=Dataset))
        self.add_input_port(InputPort("hue", port_type=int))

        self.add_output_port(OutputPort("layers", port_type=int))  # TODO: Change type
        self.outputs["layers"].output_generator = self.get_model_layers

    def get_model_layers(self):  # TODO: Implement
        raise NotImplementedError("get_model_layers not implemented!")
