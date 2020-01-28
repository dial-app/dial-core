# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from dial.datasets import DatasetLoader
from dial.utils import log

LOGGER = log.get_logger(__name__)


class DatasetsListModel(QAbstractListModel):
    def __init__(self, datasets_list: List[DatasetLoader], parent=None):
        super().__init__(parent)

        self.__datasets_list = datasets_list

        LOGGER.debug(
            "Initializing model with %d entries: %s",
            len(self.__datasets_list),
            self.__datasets_list,
        )

    def rowCount(self, parent=QModelIndex()):
        return len(self.__datasets_list)

    def index(self, row, column=0, parent=QModelIndex()):
        return self.createIndex(row, column, self.__datasets_list[row])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.__datasets_list[index.row()]}"

        return None
