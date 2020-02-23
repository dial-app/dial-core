# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from dial.misc import Dial
from dial.node_editor import Node, OutputPort

if TYPE_CHECKING:
    from .layers_editor_widget import LayersEditorWidget
    from PySide2.QtWidgets import QObject


class LayersEditorNode(Node):
    def __init__(
        self, layers_editor_widget: "LayersEditorWidget", parent: "QObject" = None
    ):
        super().__init__(
            title="Layers Editor Node", inner_widget=layers_editor_widget, parent=parent
        )

        self.add_output_port(OutputPort("layers", port_type=Dial.KerasLayerListMIME))
        self.outputs["layers"].output_generator = self.get_model_layers

    def get_model_layers(self):  # TODO: Implement
        raise NotImplementedError("get_model_layers not implemented!")
