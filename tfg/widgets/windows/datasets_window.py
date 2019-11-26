# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import (QFormLayout, QGridLayout, QLabel, QSplitter,
                               QWidget)

from tfg.datasets.dataset_loader import mnist_loader
from tfg.widgets.dataset_table import DatasetTableModel, DatasetTableView


class DatasetsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._loaded_dataset = None

        self._main_layout = QGridLayout(self)

        self._setup()

    def _setup(self):
        splitter = QSplitter()

        # TODO: Move initialization to the correct place
        self._loaded_dataset = mnist_loader()

        self._form_layout = QFormLayout(self)
        self._form_layout.addRow("Dataset name", QLabel('"Name"'))
        self._form_layout.addRow("Total items:", QLabel(f"{len(self._loaded_dataset)}"))

        model = DatasetTableModel(self)
        model.load_dataset(self._loaded_dataset)
        table_view = DatasetTableView(self)
        table_view.setModel(model)

        widget = QWidget()
        widget.setLayout(self._form_layout)
        splitter.addWidget(widget)
        splitter.addWidget(table_view)
        self._main_layout.addWidget(splitter, 0, 0)
        self._main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self._main_layout)
