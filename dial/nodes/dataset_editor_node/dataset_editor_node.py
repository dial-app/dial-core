# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import Dataset
from dial.node_editor import Node, OutputPort

from .dataset_editor_widget import DatasetEditorWidget


class DatasetEditorNode(Node):
    def __init__(self, parent=None):
        super().__init__(
            title="Dataset Node", inner_widget=DatasetEditorWidget(), parent=parent
        )

        print(self.inner_widget)

        # Ports
        self.add_output_port(OutputPort("train", port_type=Dataset))
        self.add_output_port(OutputPort("test", port_type=Dataset))

        self.outputs["train"].output_generator = self.get_train_dataset
        self.outputs["test"].output_generator = self.get_test_dataset

    def get_train_dataset(self):
        raise NotImplementedError("get_train_dataset not implemented!")

    def get_test_dataset(self):
        raise NotImplementedError("get_test_dataset not implemented!")
