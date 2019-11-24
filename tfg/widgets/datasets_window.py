# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from keras.datasets import mnist
from PySide2.QtWidgets import QGridLayout, QPushButton, QSpacerItem, QWidget

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
        self._main_layout.setColumnStretch(0, 50)
        self._main_layout.setColumnStretch(1, 50)

        # TODO: Move initialization to the correct place
        (x, y), _ = mnist.load_data()
        self._loaded_dataset = Dataset(x, y, DataType.IMAGE_ARRAY, DataType.NUMERIC)

        model = DatasetTableModel(self)
        table_view = DatasetTableView(self)
        table_view.setModel(model)

        self._main_layout.addWidget(table_view, 0, 1)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)

        dialog = LoadDatasetDialog(self)
        dialog.show()
