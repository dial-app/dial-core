# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
View for the Dataset Table model. Leverages all painting to the DatasetImteDelegate
class.
"""

from PySide2.QtWidgets import QHeaderView, QTableView

from .dataset_item_delegate import DatasetItemDelegate


class DatasetTableView(QTableView):
    """
    View for the Dataset Table model. Leverages all painting to the DatasetImteDelegate
    class.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.setItemDelegate(DatasetItemDelegate())
