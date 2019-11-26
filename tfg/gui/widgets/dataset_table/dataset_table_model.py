# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import qimage2ndarray
from PySide2.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from PySide2.QtGui import QPixmap, QPixmapCache

from tfg.datasets import Dataset, DataType


class DatasetTableModel(QAbstractTableModel):
    """
    Model representing the rows/columns of a dataset.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.__x = None
        self.__y = None

        self.__row_count = 0
        self.__column_count = 2

        self.__max_row_count = 20

        self.column_names = ("Input", "Output")

        self.__images_size = QSize(75, 75)

        self.__role_map = {
            Qt.DecorationRole: self.__data_decoration_role,
            Qt.TextAlignmentRole: self.__data_textalignment_role,
            Qt.DisplayRole: self.__data_display_role,
        }

    def load_dataset(self, dataset: Dataset):
        """
        Load new Dataset data to the model.
        """
        self.__row_count = min(self.__max_row_count, len(dataset))

        self.__x, self.__y = dataset.head(self.rowCount())

    def rowCount(self, parent=QModelIndex()):
        """
        Return the number of rows.
        """
        return self.__row_count

    def columnCount(self, parent=QModelIndex()):
        """
        Return the number of columns.
        """
        return self.__column_count

    def headerData(self, section, orientation, role):
        """
        Return the name of the headers
        """

        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return self.column_names[section]

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return f"{section}"

    def __data_display_role(self, row: int, column: int):
        if column == 0:
            return f"{self.__x[row]}"

        if column == 1:
            return f"{self.__y[row]}"

        return None

    def __data_decoration_role(self, row: int, column: int):
        pass

    def __data_textalignment_role(self, row: int, column: int):
        return Qt.AlignCenter

    def data(self, index, role=Qt.DisplayRole):
        if role in self.__role_map:
            return self.__role_map[role](index.row(), index.column())

        return None
