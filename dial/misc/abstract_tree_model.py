# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, List, Optional

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide2.QtWidgets import QWidget


class AbstractTreeNode:
    """
    Internal data structure for the AbstractTreeModel
    """

    def __init__(self, values: List[Any], parent: "AbstractTreeNode" = None):
        self.values = values
        self.parent = parent
        self.leaves: List["AbstractTreeNode"] = []

    @property
    def row(self) -> int:
        """
        Return position of current node in parent leaves
        """
        if self.parent:
            return self.parent.leaves.index(self)

        return 0

    def __getitem__(self, key: int) -> Optional["AbstractTreeNode"]:
        try:
            return self.leaves[key]
        except IndexError:
            return None

    def append(self, node: "AbstractTreeNode"):
        node.parent = self
        self.leaves.append(node)

    def column_value(self, column: int) -> Optional[Any]:
        try:
            return self.values[column]
        except IndexError:
            return None

    def columns_count(self) -> int:
        return len(self.values)


class AbstractTreeModel(QAbstractItemModel):
    """
    Easier to work model for creating trees (Used with QTreeView)
    """

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.root_node: "AbstractTreeNode" = AbstractTreeNode(["Root"])

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        """
        Returns the index corresponding to an item on the tree model.
        """

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()

        child_node = parent_node[row]

        if child_node:
            return self.createIndex(row, column, child_node)

        return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        """
        Returns the parent index of the current index.
        """

        if not index.isValid():
            return QModelIndex()

        child_node: "AbstractTreeNode" = index.internalPointer()
        parent_node = child_node.parent

        if not parent_node or parent_node == self.root_node:
            return QModelIndex()

        return self.createIndex(parent_node.row, 0, parent_node)

    def rowCount(self, index: QModelIndex) -> int:
        """
        Return the number of rows (items) under the `index`.
        """
        if index.column() > 0:
            return 0

        if not index.isValid():
            index_node = self.root_node
        else:
            index_node = index.internalPointer()

        return len(index_node.leaves)

    def columnCount(self, index: QModelIndex) -> int:
        """
        Returns the number of columns of data for the `index`.
        """
        if index.isValid():
            return index.internalPointer().columns_count()

        return self.root_node.columns_count()

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        return index.internalPointer().column_value(index.column())

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.NoItemFlags

        return super().flags(index)
