# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import IntEnum
from typing import TYPE_CHECKING, Any, Dict, List, Optional

from PySide2.QtCore import (
    QAbstractTableModel,
    QByteArray,
    QDataStream,
    QIODevice,
    QMimeData,
    QModelIndex,
    Qt,
)

from dial.utils import Dial, log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject
    from tensorflow import keras


LOGGER = log.get_logger(__name__)


class ModelTableModel(QAbstractTableModel):
    """
    Model used for composing the layers that form a Neural Network Model.

    Layer attributes (units, activations...) can be modified from this model. It also
    allows adding layers through a drop event (layers must have "Dial.KerasLayerMIME"
    MIME type)
    """

    class Column(IntEnum):
        Type = 0
        Name = 1
        Units = 2
        Trainable = 3
        Activation = 4

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__layers: List["keras.layers.Layer"] = []

        # Count the nº of occurencies of a layer name (To avoid name duplications)
        self.__layer_name_occurencies: Dict[str, int] = {}

        self.__role_map = {
            Qt.DisplayRole: self.__display_role,
            Qt.CheckStateRole: self.__checkstate_role,
        }

    def load_layers(self, layers: List["keras.layers.Layer"]):
        """
        Set a new `layers` array.
        """
        self.__layers = layers

        # Model has been reset, redraw view
        self.modelReset.emit()

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        Return the number of rows.
        """
        return len(self.__layers)

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        Return the number of columns.
        """
        return len(self.Column)

    def flags(self, index: "QModelIndex") -> int:
        """
        Flag items depending of its column.

        By default, all layers will be dragable (To allow moving layers)

        Some layers will have special flags (Like displaying a checkbox instead of text)

        Also, some layers will be editable.
        """
        if not index.isValid():
            return Qt.ItemIsDropEnabled

        general_flags = super().flags(index) | Qt.ItemIsDragEnabled

        if index.column() == self.Column.Name:
            return general_flags | Qt.ItemIsEditable

        if index.column() == self.Column.Units:
            return general_flags | Qt.ItemIsEditable

        if index.column() == self.Column.Trainable:
            return general_flags | Qt.ItemIsUserCheckable

        return general_flags

    def index(self, row: int, column: int, parent: "QModelIndex") -> "QModelIndex":
        """
        Get a `QModelIndex` representing a layer item in row X. The same layer is
        returned for all valid columns.
        """
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        return self.createIndex(row, column, self.__layers[row])

    def headerData(
        self, section: int, orientation: "Qt.Orientation", role: int = Qt.DisplayRole
    ) -> Optional[str]:
        """
        Return the name of the headers.
        Horizontal header   -> Column names
        Vertical header     -> Row nº
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

    def data(self, index: "QModelIndex", role: int = Qt.DisplayRole) -> Optional[Any]:
        """ Returns data depending on the specified role.

        Args:
            index: Index representing the item on the table.
            role: Data access role.

        Returns:
            The data of the `index` item for `role` or `None`.
        """
        if role in self.__role_map:
            return self.__role_map[role](index)

        # Center align all text
        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

        return None

    def setData(
        self, index: "QModelIndex", value: Any, role: int = Qt.EditRole
    ) -> bool:
        """
        Sets `value` on the `index` depending on the specified role.
        """
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

    def supportedDragActions(self) -> "Qt.DropActions":
        """
        Returns the supported drag actions for the layers. In this case, layers will
        only allow `Qt.MoveAction` (Move a layer from one position to another).
        """
        return Qt.MoveAction

    def supportedDropActions(self) -> "Qt.DropActions":
        """
        Returns the supported drop actions for the layers. In this case, layers will
        allow `Qt.CopyAction` (add layers from another widget), and `Qt.MoveAction` (add
        layers from the same widget).
        """
        return Qt.CopyAction | Qt.MoveAction

    def mimeTypes(self) -> List[str]:
        """
        MIME Types supported by this model. In this case, the only supported MIME type
        is the one representing a list of Keras Layer.
        """
        return [Dial.KerasLayerListMIME.value]

    def mimeData(self, indexes: List["QModelIndex"]) -> "QMimeData":
        """
        Returns a serialized object representing a List of Keras Layer. Used for
        drag/drop operations, for example.
        """
        mime_data = QMimeData()

        # Serializer
        encoded_data = QByteArray()
        stream = QDataStream(encoded_data, QIODevice.WriteOnly)

        # Write all the layers corresponding to the indexes
        for index in indexes:
            if index.isValid():
                layer = index.internalPointer()
                stream.writeQVariant(layer)

        # Store the serialized data on the MIME data
        mime_data.setData(Dial.KerasLayerListMIME.value, encoded_data)

        return mime_data

    def dropMimeData(
        self,
        mime_data: "QMimeData",
        action: "Qt.DropAction",
        row: int,
        column: int,
        parent: "QModelIndex",
    ):
        """
        Decodes and inserts the MIME data (layers) from a drop operation onto the table.
        """
        if action == Qt.IgnoreAction:
            return True

        if not mime_data.hasFormat(Dial.KerasLayerListMIME.value):
            return False

        # Get the row number where the layers will be inserted
        if row != -1:
            begin_row = row
        else:
            begin_row = self.rowCount()

        LOGGER.debug("Drop action type: %s", action)
        LOGGER.debug("Adding a new row at index %s...", begin_row)

        # Get the serilalized data from the MIME data and prepare for decoding
        encoded_data: QByteArray = mime_data.data(Dial.KerasLayerListMIME.value)
        stream = QDataStream(encoded_data, QIODevice.ReadOnly)

        # Unserialize binary data
        layers = []
        while not stream.atEnd():
            layer = stream.readQVariant()
            layers.append(layer)

        LOGGER.debug("Values to insert: %s", len(layers))
        LOGGER.debug(layers)

        # When adding new layers we must ensure that the names are all uniques
        if action == Qt.CopyAction:
            self.__set_unique_layer_names(layers)

        # Insert the decoded layers on the model
        self.insertRows(begin_row, len(layers), self.createIndex(begin_row, 0, layers))

        return True

    def insertRows(self, row: int, count: int, parent=QModelIndex()) -> bool:
        """
        Insert new rows onto the model. `parent.internalPointer()` must be a list of the
        new layers to insert.
        """
        LOGGER.debug("Insert rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())

        self.beginInsertRows(QModelIndex(), row, row + count - 1)

        new_layers: List = parent.internalPointer()

        # A suffix is added to each layer to make the names unique.
        # So, the first time a layer with name "A" is added, it will be called "A_1",
        # the second time "A_2", the third time "A_3"...

        self.__layers[row:row] = new_layers

        self.endInsertRows()

        LOGGER.debug("Insert rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        return True

    def removeRows(self, row: int, count: int, index=QModelIndex()) -> bool:
        """
        Remove rows from the model. Rows being deleted must be consecutive.
        """
        if not index.isValid():
            return False

        LOGGER.debug("Remove rows BEGIN: row %s, %s items", row, count)
        LOGGER.debug("Previous model size: %s", self.rowCount())
        self.beginRemoveRows(QModelIndex(), row, row + count - 1)

        # Remove the layer name from the unique names counter
        # layer_name = index.internalPointer().name.split("_")[0]
        # self.__layer_name_occurencies[layer_name] -= 1

        # Remove rows from the layers array
        del self.__layers[row : row + count]

        self.endRemoveRows()
        LOGGER.debug("Remove rows END")
        LOGGER.debug("New model size: %s", self.rowCount())

        return True

    def moveRows(
        self,
        source_parent: "QModelIndex",
        source_row: int,
        count: int,
        destination_parent: "QModelIndex",
        destination_child: int,
    ) -> bool:
        LOGGER.debug(
            "Move rows BEGIN: row %s, %s items to %s",
            source_row,
            count,
            destination_child,
        )

        self.beginMoveRows(
            source_parent,
            source_row,
            source_row + count - 1,
            destination_parent,
            destination_child,
        )

        self.endMoveRows()

        return True

    def __display_role(self, index: "QModelIndex") -> Optional[str]:
        """
        Returns the text representation of the index value.
        """
        if not index.isValid():
            return None

        layer = index.internalPointer()

        try:
            if index.column() == self.Column.Type:
                return str(type(layer).__name__)

            if index.column() == self.Column.Name:
                return str(layer.name)

            if index.column() == self.Column.Units:
                return str(layer.units)

            if index.column() == self.Column.Activation:
                return str(layer.activation.__name__)

        except AttributeError:
            pass

        return None

    def __checkstate_role(self, index: "QModelIndex") -> Optional["Qt.CheckState"]:
        """
        Returns a checkbox representatino of the index value.
        """
        if not index.isValid():
            return None

        if index.flags() & Qt.ItemIsUserCheckable:
            return Qt.Checked if index.internalPointer().trainable else Qt.Unchecked

        return None

    def __set_unique_layer_names(self, layers: "keras.layers.Layer"):
        for layer in layers:
            layer_name = layer.name.split("_")[0]
            self.__layer_name_occurencies.setdefault(layer_name, 0)
            self.__layer_name_occurencies[layer_name] += 1

            layer._name = f"{layer_name}_{self.__layer_name_occurencies[layer_name]}"
