# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QHeaderView, QTableView,QMenu

from .dataset_item_delegate import DatasetItemDelegate

if TYPE_CHECKING:
    from PySide2.QtWidgets import QWidget


class DatasetTableView(QTableView):
    """
    View for the Dataset Table model. Leverages all painting to the DatasetImteDelegate
    class.
    """

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.setItemDelegate(DatasetItemDelegate())

    def contextMenuEvent(self, event: "QContextMenuEvent"):
        """Show a context menu for modifying dataset entries."""
        menu = QMenu(parent=self)

        menu.popup(event.globalPos())
        menu.addAction("Remove entries", lambda: self.deleteSelectedRows())


    def deleteSelectedRows(self):
        # When a row is deleted, the new row index is the last row index - 1
        # That's why we have an i variable on this loop, which represents the amount of
        # rows that have been deleted
        for i, row_index in enumerate(self.selectedIndexes()):
            self.model().removeRow(row_index.row() - i, row_index)
