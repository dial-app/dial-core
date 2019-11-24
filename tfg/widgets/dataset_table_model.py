# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt
from PySide2.QtGui import QColor


class DatasetTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.dataset = None

        self.row_count = 2
        self.column_count = 2

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        # Header names
        if orientation == Qt.Horizontal:
            return ("Date", "Magnitude")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            return f"{row} {column}"

        if role == Qt.BackgroundRole:
            return QColor(Qt.white)

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None
