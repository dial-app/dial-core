# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from keras.datasets import mnist
from PySide2.QtWidgets import QPushButton, QSpacerItem, QVBoxLayout, QWidget

from tfg.datasets import Dataset, DataType
from tfg.widgets.dataset_view import DatasetView
from tfg.widgets.load_dataset_dialog import LoadDatasetDialog


class DatasetsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._loaded_dataset = None

        self._main_layout = QVBoxLayout(self)

        self._setup()

    def _setup(self):
        # TODO: Move initialization to the correct place
        (x, y), _ = mnist.load_data()
        self._loaded_dataset = Dataset(x, y, DataType.IMAGE_ARRAY, DataType.NUMERIC)

        self._main_layout.addWidget(DatasetView(self._loaded_dataset, self))

        self.setLayout(self._main_layout)

        dialog = LoadDatasetDialog(self)
        dialog.show()
