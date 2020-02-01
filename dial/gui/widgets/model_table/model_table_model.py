# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import List, Optional

from PySide2.QtCore import (
    QAbstractTableModel,
    QByteArray,
    QDataStream,
    QIODevice,
    QMimeData,
    QModelIndex,
    Qt,
)
from tensorflow import keras

from dial.misc import Dial
from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelTableModel(QAbstractTableModel):
    """
    Model representing the layers/structure of a model (neural network)
    """

    class Column(IntEnum):
        Type = 0
        Name = 1
        Units = 2
        Trainable = 3
        Activation = 4

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__layers = []

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            Qt.CheckStateRole: self.__checkstate_role,
        }

    def load_model(self, model):
        self.__layers = [l for l in model.layers]

        # Model has been reset, redraw view
        self.modelReset.emit()

    def rowCount(self, parent=QModelIndex()):
        """
        Return the number of rows.
        """
        return len(self.__layers)

    def columnCount(self, parent=QModelIndex()):
        """
        Return the number of columns.
        """
        return len(self.Column)

    def flags(self, index: QModelIndex):
        if not index.isValid():
            return Qt.ItemIsEnabled | Qt.ItemIsDropEnabled

        if index.column() == self.Column.Trainable:
            return super().flags(index) | Qt.ItemIsUserCheckable

        if index.column() == self.Column.Type:
            return super().flags(index)

        if index.column() == self.Column.Activation:
            return super().flags(index)

        return super().flags(index) | Qt.ItemIsEditable

    def index(self, row, column, parent):
        return self.createIndex(row, column, self.__layers[row])

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

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(self, index: QModelIndex, value, role):
        if not index.isValid():
            return False

        layer = index.internalPointer()

        if role == Qt.CheckStateRole:
            if index.column() == self.Column.Trainable:
                layer.trainable = bool(value)

        if role == Qt.EditRole:
            if index.column() == self.Column.Name:
                layer._name = str(value)

            if index.column() == self.Column.Units:
                layer.units = int(value)

        LOGGER.info("New layer config: %s", layer.get_config())

        return True

    def supportedDragActions(self):
        return Qt.CopyAction

    def mimeTypes(self) -> List[str]:
        return [Dial.KerasLayerDictMIME.value]

    def dropMimeData(
        self, data: QMimeData, action, row: int, column: int, parent: QModelIndex
    ):
        if action == Qt.IgnoreAction:
            return True

        if not data.hasFormat(Dial.KerasLayerDictMIME.value):
            return False

        # Get row number where the data will be inserted
        if row != -1:
            begin_row = row
        elif parent.isValid():
            begin_row = parent.row
        else:
            begin_row = self.rowCount()

        LOGGER.debug("Adding a new row at index %s...", begin_row)

        # Decode data
        encoded_data: QByteArray = data.data(Dial.KerasLayerDictMIME.value)
        stream = QDataStream(encoded_data, QIODevice.ReadOnly)

        items = []

        while not stream.atEnd():
            layer_dict = stream.readQVariant()
            layer = keras.layers.deserialize(layer_dict)
            items.append(layer)

        LOGGER.debug("Values to insert: %s", len(items))
        LOGGER.debug(items)

        self.insertRows(begin_row, len(items), self.createIndex(begin_row, 0, items))

        return True

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        # TODO: Insert several rows?
        self.layoutAboutToBeChanged.emit()

        LOGGER.debug("Insert rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())
        self.beginInsertRows(parent, row, row + count - 1)

        self.__layers[row:row] = parent.internalPointer()

        self.endInsertRows()
        LOGGER.debug("Insert rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        self.layoutChanged.emit()

        return True

    def __display_role(self, index: QModelIndex) -> Optional[str]:
        """
        Return the text representation of the cell value.
        """
        if not index.isValid():
            return None

        layer = index.internalPointer()

        if index.column() == self.Column.Type:
            return str(type(layer).__name__)

        if index.column() == self.Column.Name:
            return str(layer.name)

        if index.column() == self.Column.Units:
            return str(layer.units)

        if index.column() == self.Column.Activation:
            return str(layer.activation.__name__)

        # if index.column() == self.Column.Trainable:
        #     return ""

        # if index.column() == self.Column.Param:
        #     return str(self.__layers[index.row()].count_params())

        return None

    def __checkstate_role(self, index: QModelIndex):
        if not index.isValid():
            return None

        if index.flags() & Qt.ItemIsUserCheckable:
            return Qt.Checked if index.internalPointer().trainable else Qt.Unchecked

        return None
