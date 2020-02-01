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

from dial.misc import AbstractTreeModel, AbstractTreeNode, Dial


class LayerNode(AbstractTreeNode):
    def __init__(self, name, layer, parent: AbstractTreeNode = None):
        super().__init__(
            [name, layer], parent,
        )

    @property
    def name(self) -> Optional[str]:
        return self.values[0]

    @property
    def layer(self):
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
        basic_layers = TitleNode("Basic Layers")
        basic_layers.append(LayerNode("Dense", keras.layers.Dense(10)))

        activation_layers = TitleNode("Activation Layers")
        activation_layers.append(LayerNode("Linear", keras.layers.Activation("linear")))
        activation_layers.append(LayerNode("ELU", keras.layers.Activation("elu")))

        self.root_node.append(basic_layers)
        self.root_node.append(activation_layers)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if isinstance(index.internalPointer(), LayerNode):
            return super().flags(index) | Qt.ItemIsDragEnabled | Qt.ItemIsDropEnabled

        return super().flags(index)

    def mimeTypes(self) -> List[str]:
        return [Dial.KerasLayerDictMIME.value]

    def mimeData(self, indexes):
        mime_data = QMimeData()
        encoded_data = QByteArray()

        stream = QDataStream(encoded_data, QIODevice.WriteOnly)

        for index in indexes:
            if index.isValid():
                layer_node = index.internalPointer()

                stream.writeQVariant(layer_node.layer)

        mime_data.setData(Dial.KerasLayerDictMIME.value, encoded_data)

        return mime_data
