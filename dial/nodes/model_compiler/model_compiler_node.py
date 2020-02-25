# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from tensorflow.keras import Model

from dial.base.datasets import Dataset
from dial.node_editor import InputPort, Node, OutputPort
from dial.utils import Dial

if TYPE_CHECKING:
    from .model_compiler_widget import ModelCompilerWidget


class ModelCompilerNode(Node):
    def __init__(self, model_compiler_widget: "ModelCompilerWidget"):
        super().__init__(
            title="Model Compiler Node", inner_widget=model_compiler_widget,
        )

        # Ports
        self.add_input_port(InputPort("dataset", port_type=Dataset))
        self.add_input_port(InputPort("layers", port_type=Dial.KerasLayerListMIME))

        self.add_output_port(OutputPort("model", port_type=Model))
        self.outputs["model"].output_generator = self.get_model

    def get_model(self):
        raise NotImplementedError("get_model is not implemented!")
