# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractTableModel, QModelIndex, QSize, Qt
from PySide2.QtGui import QPixmapCache

from dial.datasets import Dataset
from dial.misc import Dial


class DatasetTableModel(QAbstractTableModel):
    """
    Model representing the rows/columns of a dataset.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__x = None
        self.__y = None
        self.__x_type = None
        self.__y_type = None

        self.__row_count = 0
        self.__column_count = 2

        self.__max_row_count = 100

        self.column_names = ("Input", "Output")

        self.__images_size = QSize(75, 75)

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            Dial.RawRole: self.__data_raw_role,
            Dial.TypeRole: self.__data_type_role,
        }

    def load_dataset(self, dataset: Dataset):
        """
        Load new Dataset data to the model.
        """
        self.__row_count = min(self.__max_row_count, len(dataset))

        self.__x, self.__y = dataset.head(self.rowCount())
        self.__x_type = dataset.x_type
        self.__y_type = dataset.y_type

        QPixmapCache.clear()

        # Model has been reset, redraw view
        self.modelReset.emit()

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

        return None

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        Return the corresponding data depending on the specified role.
        """

        if role in self.__role_map:
            return self.__role_map[role](index.row(), index.column())

        return None

    def __display_role(self, row: int, column: int):
        """
        Return the text representation of the cell value.
        """
        if column == 0:
            return self.__x_type.display(self.__x[row])

        if column == 1:
            return self.__y_type.display(self.__y[row])

        return None

    def __data_raw_role(self, row: int, column: int):
        """
        Return the raw value of the cell.
        """
        if column == 0:
            return self.__x[row]

        if column == 1:
            return self.__y[row]

        return None

    def __data_type_role(self, row: int, column: int):
        """
        Return the type of the data on the cell.
        """
        if column == 0:
            return self.__x_type

        if column == 1:
            return self.__y_type

        return None
