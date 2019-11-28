# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the dataset related operations (Visualization, loading...)
"""

from PySide2.QtWidgets import (QFormLayout, QGridLayout, QLabel, QSplitter,
                               QWidget)

from tfg.datasets.predefined_dataset import MnistDataset
from tfg.gui.widgets.dataset_table import DatasetTableModel, DatasetTableView
from tfg.gui.widgets.predefined_datasets_list import PredefinedDatasetsDialog


class DatasetsWindow(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Attributes
        self.__loaded_dataset = None

        self.__dataset_model = DatasetTableModel(self)
        self.__dataset_view = DatasetTableView(self)
        self.__dataset_view.setModel(self.__dataset_model)

        # Widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__dataset_name_label = QLabel("")
        self.__dataset_len_label = QLabel("")

        self.__setup_ui()

    def __setup_ui(self):
        splitter = QSplitter()

        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items", self.__dataset_len_label)

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__dataset_view)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)
