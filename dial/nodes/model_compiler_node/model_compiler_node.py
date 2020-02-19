# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import Dataset
from dial.misc import Dial
from dial.node_editor import InputPort, Node


class ModelCompilerNode(Node):
    def __init__(self, parent=None):
        super().__init__(
            title="Model Compiler Node", parent=parent,
        )

        # Ports
        self.add_input_port(InputPort("dataset", port_type=Dataset))
        self.add_input_port(InputPort("layers", port_type=Dial.KerasLayerListMIME))

        # self.add_output_port(OutputPort("layers", port_type=int))  # TODO: Change type
        # self.outputs["layers"].output_generator = self.get_model_layers

    # def get_model_layers(self):  # TODO: Implement
    #     raise NotImplementedError("get_model_layers not implemented!")
