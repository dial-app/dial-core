# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the dataset related operations (Visualization, loading...)
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import (QFormLayout, QGridLayout, QLabel, QPushButton,
                               QSplitter, QWidget)

from tfg.datasets import Dataset
from tfg.datasets.predefined_dataset import PredefinedDatasetLoader
from tfg.gui.widgets.dataset_table import DatasetTableModel, DatasetTableView
from tfg.gui.widgets.predefined_datasets_list import PredefinedDatasetsDialog


class DatasetsWindow(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, parent):
        super().__init__(parent)

        # Attributes
        self.__dataset = None

        self.__dataset_model = DatasetTableModel(self)
        self.__dataset_view = DatasetTableView(self)
        self.__dataset_view.setModel(self.__dataset_model)

        # Widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__dataset_name_label = QLabel("")
        self.__dataset_len_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__setup_ui()

        self.__dataset_loader_button.clicked.connect(self.load_predefined_dataset)

    def __setup_ui(self):
        splitter = QSplitter()

        self.__options_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items", self.__dataset_len_label)
        self.__options_layout.addRow(
            "Load predefined dataset", self.__dataset_loader_button
        )

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__dataset_view)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def load_predefined_dataset(self):
        """
        Select and load a predefined dataset from a Dialog list.
        """
        dataset_loader_dialog = PredefinedDatasetsDialog(self)

        accepted = dataset_loader_dialog.exec_()

        if accepted:
            dataset_loader = dataset_loader_dialog.selected_loader()
            self.__set_dataset(dataset_loader)

    def __set_dataset(self, dataset_loader: PredefinedDatasetLoader):
        """
        Set a new Dataset, updating the model, view, and labels.
        """

        self.__dataset, _ = dataset_loader.load()

        self.__dataset_model.load_dataset(self.__dataset)

        print("Dataset loaded")

        self.__dataset_name_label.setText(str(dataset_loader.name))
        self.__dataset_len_label.setText(str(len(self.__dataset)))
