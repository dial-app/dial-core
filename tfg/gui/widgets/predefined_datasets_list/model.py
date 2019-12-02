# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from tfg.datasets.predefined_dataset import (BostonHousingLoader,
                                             Cifar10Loader, FashionMnistLoader,
                                             MnistLoader)
from tfg.utils import Tfg


class PredefinedDatasetsListModel(QAbstractListModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.predefined_datasets = [
            MnistLoader(),
            Cifar10Loader(),
            BostonHousingLoader(),
            FashionMnistLoader(),
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self.predefined_datasets)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.predefined_datasets[index.row()]}"

        if role == Tfg.RawRole:
            return self.predefined_datasets[index.row()]

        return None
