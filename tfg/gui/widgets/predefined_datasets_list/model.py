# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QAbstractListModel, QModelIndex, Qt

from tfg.datasets.predefined_dataset import (BostonHousingDataset,
                                             Cifar10Dataset, MnistDataset)


class PredefinedDatasetsListModel(QAbstractListModel):
    def __init__(self, parent):
        super().__init__(parent)

        self.predefined_datasets = [
            MnistDataset(),
            Cifar10Dataset(),
            BostonHousingDataset(),
        ]

    def rowCount(self, parent=QModelIndex()):
        return len(self.predefined_datasets)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return f"{self.predefined_datasets[index.row()]}"

        return None
