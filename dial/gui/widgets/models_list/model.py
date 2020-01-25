# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import List

from dial.datasets import DatasetLoader
from dial.misc import Dial
from dial.utils import log
from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

LOGGER = log.get_logger(__name__)


class ModelsListModel(QAbstractListModel):
    def __init__(self, models_list=None, parent=None):
        super().__init__(parent)

        self.__models_list = models_list

    def rowCount(self, parent=QModelIndex()):
        return len(self.__models_list)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.__models_list[index.row()]}"

        if role == Dial.RawRole:
            return self.__models_list[index.row()]

        return None
