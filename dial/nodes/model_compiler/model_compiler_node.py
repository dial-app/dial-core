# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from tensorflow.keras import Model

from dial.datasets import Dataset
from dial.misc import Dial
from dial.node_editor import InputPort, Node, OutputPort

if TYPE_CHECKING:
    from PySide2.QtCore import QObject
    from .model_compiler_widget import ModelCompilerWidget


class ModelCompilerNode(Node):
    def __init__(
        self, model_compiler_widget: "ModelCompilerWidget", parent: "QObject" = None
    ):
        super().__init__(
            title="Model Compiler Node",
            inner_widget=model_compiler_widget,
            parent=parent,
        )

        # Ports
        self.add_input_port(InputPort("dataset", port_type=Dataset))
        self.add_input_port(InputPort("layers", port_type=Dial.KerasLayerListMIME))

        self.add_output_port(OutputPort("model", port_type=Model))
        self.outputs["model"].output_generator = self.get_model

    def get_model(self):
        raise NotImplementedError("get_model is not implemented!")
