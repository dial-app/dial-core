# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


"""This module has the necessary components for working with a Tree Based hierarchy for
Qt Model/View architecture.

First, the AbstractTreeNode class is the basic construction item of the model. It can
store any list of values, arranged later on different columns.

Then, the AbstractTreeModel class is the base class used for Tree models. Has
convenience functions for adding and accessing the tree nodes.
"""


from typing import TYPE_CHECKING, Any, List, Optional

from PySide2.QtCore import QAbstractItemModel, QModelIndex, Qt

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class AbstractTreeNode:
    """The AbstractTreeNode class provides a container to store elements on a
    tree-based hierarchy of nodes.

    Each node must have a parent and can have several children (or leaves).
    """

    def __init__(self, values: List[Any], parent: Optional["AbstractTreeNode"] = None):
        """
        Args:
            values: Data to store on the node.
            parent: The parent node of this node.
        """
        self.values = values
        self.parent = parent
        self.leaves: List["AbstractTreeNode"] = []

    @property
    def row(self) -> int:
        """ Returns the position of this node with respect to its parent children.

        If the node has no parent (topmost node) the returned position is always 0.

        Examples:
            parentNode
                |- nodeA    (row() -> 0)
                |- nodeB    (row() -> 1)
                |- nodeC    (row() -> 2)

        Returns:
            Position of the current node.
        """
        if self.parent:
            return self.parent.leaves.index(self)

        return 0

    def __getitem__(self, position: int) -> Optional["AbstractTreeNode"]:
        """Gets the child node at position `position`.

        Args:
            position: The position of the child node to access.

        Returns:
            The child node or None if there isn't a child at that position.
        """
        try:
            return self.leaves[position]
        except IndexError:
            return None

    def append(self, node: "AbstractTreeNode"):
        """Adds a new node to the list of child nodes.

        Args:
            node: The new `AbstractTreeNode` object to append.
        """
        node.parent = self
        self.leaves.append(node)

    def column_value(self, column: int) -> Optional[Any]:
        """Returns the data stored on the node at position `column`.

        Args:
            column: The position of the data list.

        Returns:
            The stored data or None if couldn't access.
        """
        try:
            return self.values[column]
        except IndexError:
            return None

    def columns_count(self) -> int:
        """Returns the number of columns of data stored on this node."""
        return len(self.values)


class AbstractTreeModel(QAbstractItemModel):
    """The AbstractTreeModel class provides the abstract interface for tree model classes.

    It defines the standard interface that tree models must use to be able to
    interoperate with other components in the model/view architecture.

    Attributes:
        root_node: Base node of all nodes.
    """

    def __init__(self, parent: "QWidget"):
        super().__init__(parent)

        self.root_node: "AbstractTreeNode" = AbstractTreeNode(["Root"])

    def index(self, row: int, column: int, parent: "QModelIndex") -> "QModelIndex":
        """ Returns the index corresponding to an item in the tree model.

        A valid index must have a row/column inside bounds

        Returns:
            An index representing an unique node on the tree model.
        """

        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if parent.isValid():
            parent_node = parent.internalPointer()
        else:
            parent_node = self.root_node

        child_node = parent_node[row]

        if child_node:
            return self.createIndex(row, column, child_node)

        return QModelIndex()

    def parent(self, index: "QModelIndex") -> "QModelIndex":
        """Returns an index representing the parent node of `index`.

        Args:
            index: The index to get the parent from.
        """
        if not index.isValid():
            return QModelIndex()

        child_node: "AbstractTreeNode" = index.internalPointer()
        parent_node = child_node.parent

        # Root node returns an invalid index too
        if not parent_node or parent_node == self.root_node:
            return QModelIndex()

        # Column value doesn't matter for this, so we just put a 0
        return self.createIndex(parent_node.row, 0, parent_node)

    def rowCount(self, index: "QModelIndex") -> int:
        """Returns the number of rows (items) under `index`."""
        if index.column() > 0:
            return 0

        if not index.isValid():
            index_node = self.root_node
        else:
            index_node = index.internalPointer()

        return len(index_node.leaves)

    def columnCount(self, index: "QModelIndex") -> int:
        """Returns the number of columns of data for `index`."""
        if index.isValid():
            return index.internalPointer().columns_count()

        return self.root_node.columns_count()

    def data(self, index: "QModelIndex", role=Qt.DisplayRole) -> Optional[Any]:
        """Returns the data for `index`.

        Data can be only accessed using `Qt.DisplayRole` role.
        """
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        return index.internalPointer().column_value(index.column())
