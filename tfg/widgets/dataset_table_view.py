# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QHeaderView, QStyledItemDelegate,
                               QStyleOptionViewItem, QTableView)


class DatasetTableView(QTableView):
    def __init__(self, parent):
        super().__init__(parent)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def viewOptions(self):
        option = super().viewOptions()
        option.decorationAlignment = Qt.AlignCenter

        # option.decorationPosition = QStyleOptionViewItem.Top

        return option
