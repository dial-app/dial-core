# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List, Optional

from PySide2.QtCore import (
    QByteArray,
    QDataStream,
    QIODevice,
    QMimeData,
    QModelIndex,
    Qt,
)
from PySide2.QtWidgets import QWidget
from tensorflow import keras

from dial.misc import AbstractTreeModel, AbstractTreeNode


class LayerNode(AbstractTreeNode):
    def __init__(self, layer_type, parent: AbstractTreeNode = None):
        super().__init__([layer_type.__name__, layer_type(10).get_config()], parent)

    @property
    def name(self) -> Optional[str]:
        return self.values[0]

    @property
    def config(self):
        return self.values[1]


class TitleNode(AbstractTreeNode):
    def __init__(self, name, parent: AbstractTreeNode = None):
        super().__init__([name], parent)

    @property
    def name(self) -> str:
        return self.values[0]


class LayersTreeModel(AbstractTreeModel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setup_model_data()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def setup_model_data(self):
        title_node = TitleNode("Basic Layers")
        title_node.append(LayerNode(keras.layers.Dense))

        self.root_node.append(title_node)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if isinstance(index.internalPointer(), LayerNode):
            return super().flags(index) | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

        return super().flags(index)

    def mimeTypes(self) -> List[str]:
        return ["application/layer"]

    def mimeData(self, indexes):
        mime_data = QMimeData()
        encoded_data = QByteArray()

        stream = QDataStream(encoded_data, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                layer_node = index.internalPointer()

                stream.writeQVariant(
                    {"class_name": layer_node.name, "config": layer_node.config}
                )

        mime_data.setData("application/layer", encoded_data)

        return mime_data
