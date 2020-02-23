# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QHeaderView, QTableView

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
