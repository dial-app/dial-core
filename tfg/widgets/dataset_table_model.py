# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from PySide2.QtGui import QColor, QImage, QPixmap, QPixmapCache

from tfg.datasets import DataType


class DatasetTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.dataset = None
        self.x = None
        self.y = None

        self.row_count = 0
        self.column_count = 2
        self.images_size = QSize(75, 75)

    def load_dataset(self, dataset):
        self.dataset = dataset

        self.row_count = 20

        self.x, self.y = self.dataset.head(self.row_count)

    def rowCount(self, parent=QModelIndex()):
        return self.row_count

    def columnCount(self, parent=QModelIndex()):
        return self.column_count

    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return None

        # Header names
        if orientation == Qt.Horizontal:
            return ("Input", "Output")[section]
        else:
            return f"{section}"

    def data(self, index, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DecorationRole:
            if column == 0:
                if self.dataset.x_type == DataType.IMAGE_ARRAY:
                    pm = QPixmap()
                    if not QPixmapCache.find(f"input_{row}", pm):
                        image_data = self.x[row]
                        pm = QPixmap.fromImage(
                            QImage(
                                image_data,
                                image_data.shape[0],
                                image_data.shape[1],
                                QImage.Format_Grayscale8,
                            )
                        )

                        QPixmapCache.insert(f"input_{row}", pm)

                    return pm

                return f"1"

        if role == Qt.DisplayRole:
            if column == 0 and self.dataset.x_type != DataType.IMAGE_ARRAY:
                print(f"{self.x[row]}")
                return f"{self.x[row]}"

            if column == 1:
                return f"{self.y[row]}"

        if role == Qt.TextAlignmentRole:
            if column == 0 and self.dataset.x_type == DataType.NUMERIC_ARRAY:
                return Qt.AlignLeft

            return Qt.AlignCenter

        return None
