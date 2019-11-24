# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from keras.datasets import mnist
from PySide2.QtWidgets import (QGridLayout, QPushButton, QSpacerItem,
                               QSplitter, QWidget)

from tfg.datasets import Dataset, DataType
from tfg.widgets.dataset_table_model import DatasetTableModel
from tfg.widgets.dataset_table_view import DatasetTableView
from tfg.widgets.load_dataset_dialog import LoadDatasetDialog


class DatasetsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._loaded_dataset = None

        self._main_layout = QGridLayout(self)

        self._setup()

    def _setup(self):
        splitter = QSplitter()

        # TODO: Move initialization to the correct place
        (x, y), _ = mnist.load_data()
        self._loaded_dataset = Dataset(x, y, DataType.IMAGE_ARRAY, DataType.NUMERIC)

        model = DatasetTableModel(self)
        model.load_dataset(self._loaded_dataset)
        table_view = DatasetTableView(self)
        table_view.setModel(model)

        splitter.addWidget(QPushButton("space"))
        splitter.addWidget(table_view)
        self._main_layout.addWidget(splitter, 0, 0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)

        dialog = LoadDatasetDialog(self)
        dialog.show()
