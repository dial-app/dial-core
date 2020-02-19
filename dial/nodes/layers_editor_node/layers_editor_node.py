# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.misc import Dial
from dial.node_editor import Node, OutputPort

from .layers_editor_widget import LayersEditorWidget


class LayersEditorNode(Node):
    def __init__(self, parent=None):
        super().__init__(
            title="Layers Editor Node",
            inner_widget=LayersEditorWidget(),
            parent=parent,
        )

        self.add_output_port(OutputPort("layers", port_type=Dial.KerasLayerListMIME))
        self.outputs["layers"].output_generator = self.get_model_layers

    def get_model_layers(self):  # TODO: Implement
        raise NotImplementedError("get_model_layers not implemented!")
