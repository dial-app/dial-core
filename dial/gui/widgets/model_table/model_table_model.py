# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt


class ModelTableModel(QAbstractTableModel):
    """
    Model representing the layers/structure of a model (neural network)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = None

        self.column_names = ("Type", "Name", "Output Shape", "Param", "Trainable")
        self.__row_count = 0
        self.__column_count = len(self.column_names)

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
        }

    def load_model(self, model):
        self.__model = model

        self.__row_count = len(model.layers)

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
            return type(self.__model.layers[row]).__name__

        if column == 1:
            return self.__model.layers[row].name

        if column == 2:
            return str(self.__model.layers[row].get_output_shape_at(0))

        if column == 3:
            return self.__model.layers[row].count_params()

        if column == 4:
            return self.__model.layers[row].trainable

        return None
