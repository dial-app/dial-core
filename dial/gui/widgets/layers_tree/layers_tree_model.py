# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt


class TreeNode:
    def __init__(self, parent, row):
        self.name = "heu"
        self.parent = parent
        self.row = row
        self.leaves = []


class LayersTreeModel(QAbstractItemModel):
    """
    Model representing a list of all the layers that can be use to compose neural
    network models.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        a = TreeNode(parent=None, row=0)
        TreeNode(parent=a, row=0)
        TreeNode(parent=a, row=1)
        self.root_nodes = [TreeNode(parent=None, row=0), a]

    def index(self, row, column, parent):
        if not parent.isValid():
            return self.createIndex(row, column, self.root_nodes[row])

        parent_node = parent.internalPointer()
        return self.createIndex(row, column, parent_node.leaves[row])

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        node = index.internalPointer()

        if node.parent is None:
            return QModelIndex()
        else:
            return self.createIndex(node.parent.row, 0, node.parent)

    def reset(self):
        self.root_nodes = [TreeNode(parent=None, row=0)]
        super().reset(self)

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.root_nodes)

        node = parent.internalPointer()
        return len(node.leaves)

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()
        if role == Qt.DisplayRole and index.column() == 0:
            return node.name

        return None
