# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

from PySide2.QtCore import QModelIndex
from PySide2.QtWidgets import QWidget

from dial.misc import AbstractTreeModel, AbstractTreeNode


class LayerNode(AbstractTreeNode):
    def __init__(self, name, parent: AbstractTreeNode = None):
        super().__init__([name], parent)

    @property
    def name(self) -> Optional[str]:
        return self.__values[0]


class TitleNode(AbstractTreeNode):
    def __init__(self, name, parent: AbstractTreeNode = None):
        super().__init__([name], parent)

    @property
    def name(self) -> str:
        return self.__values[0]


class LayersTreeModel(AbstractTreeModel):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setup_model_data()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def setup_model_data(self):
        title_node = TitleNode("BasicLayers")
        title_node.append(LayerNode("Dense"))
        title_node.append(LayerNode("Activation"))

        self.root_node.append(title_node)
