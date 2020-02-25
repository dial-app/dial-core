# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Any, Optional

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from dial.utils import log

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject

    # from dial.base.datasets import DatasetLoader


LOGGER = log.get_logger(__name__)


class DatasetsListModel(QAbstractListModel):
    def __init__(self, datasets_list, parent: "QObject" = None):
        super().__init__(parent)

        self.__datasets_list = datasets_list

        LOGGER.debug(
            "Initializing model with %d entries: %s",
            len(self.__datasets_list),
            self.__datasets_list,
        )

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.__datasets_list)

    def index(self, row: int, column: int = 0, parent=QModelIndex()) -> "QModelIndex":
        return self.createIndex(row, column, self.__datasets_list[row])

    def data(self, index, role=Qt.DisplayRole) -> Optional[Any]:
        if role == Qt.DisplayRole:
            return f"{self.__datasets_list[index.row()]}"

        return None
