# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum

from PySide2.QtCore import QAbstractTableModel, QModelIndex, Qt

from dial.misc import Dial


class ModelTableModel(QAbstractTableModel):
    """
    Model representing the layers/structure of a model (neural network)
    """

    class Column(IntEnum):
        Type = 0
        Name = 1
        OutputShape = 2
        Param = 3
        Trainable = 4

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__layers = None

        self.__row_count = 0
        self.__column_count = len(self.Column)

        self.__role_map = {
            Dial.RawRole: self.__raw_role,
            Qt.DisplayRole: self.__display_role,
            Qt.CheckStateRole: self.__checkstate_role,
        }

    def load_model(self, model):
        self.__layers = [l for l in model.layers]

        self.__row_count = len(self.__layers)

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

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled

        if index.column() == self.Column.Trainable:
            return super().flags(index) | Qt.ItemIsUserCheckable

        if index.column() == self.Column.Name:
            return super().flags(index) | Qt.ItemIsEditable

        return Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        """
        Return the name of the headers
        """

        if role != Qt.DisplayRole:
            return None

        # Column header must have their respective names
        if orientation == Qt.Horizontal:
            return str(self.Column(section).name)

        # Row header will have the row number as name
        if orientation == Qt.Vertical:
            return str(section)

        return None

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        """
        Return the corresponding data depending on the specified role.
        """

        if role in self.__role_map:
            return self.__role_map[role](index)

        return None

    def supportedDragActions(self):
        return Qt.CopyAction

    def setData(self, index: QModelIndex, value, role):
        if not index.isValid():
            return False

        if role == Qt.CheckStateRole:
            if index.column() == self.Column.Trainable:
                self.__layers[index.row()].trainable = value

        if role == Qt.EditRole:
            if index.column() == self.Column.Name:
                self.__layers[index.row()]._name = value

        return True

    def __display_role(self, index: QModelIndex):
        """
        Return the text representation of the cell value.
        """
        if index.column() == self.Column.Trainable:
            return ""

        return str(index.data(Dial.RawRole))

    def __raw_role(self, index: QModelIndex):
        if index.column() == self.Column.Type:
            return type(self.__layers[index.row()]).__name__

        if index.column() == self.Column.Name:
            return self.__layers[index.row()].name

        if index.column() == self.Column.OutputShape:
            return self.__layers[index.row()].get_output_shape_at(0)

        if index.column() == self.Column.Param:
            return self.__layers[index.row()].count_params()

        if index.column() == self.Column.Trainable:
            return self.__layers[index.row()].trainable

        return None

    def __checkstate_role(self, index: QModelIndex):
        if index.flags() & Qt.ItemIsUserCheckable:
            return Qt.Checked if index.data(Dial.RawRole) else Qt.Unchecked

        return None
