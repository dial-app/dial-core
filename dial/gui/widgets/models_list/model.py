# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelLoadersListModel(QAbstractListModel):
    def __init__(self, models_list=None, parent=None):
        super().__init__(parent)

        self.__models_list = models_list

    def rowCount(self, parent=QModelIndex()):
        return len(self.__models_list)

    def index(self, row, column=0, parent=QModelIndex()):
        return self.createIndex(row, column, self.__models_list[row])

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.__models_list[index.row()]}"

        return None
