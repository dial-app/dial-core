# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)

from .datasets_list import PredefinedDatasetsList

if TYPE_CHECKING:
    from .dataset_table import TrainTestTabs


class DatasetEditorWidget(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, train_test_tabs: "TrainTestTabs", parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__train_test_tabs = train_test_tabs
        self.__train_test_tabs.setParent(self)

        self.__dataset_name_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__train_len_label = QLabel("")
        self.__test_len_label = QLabel("")

        # Configure interface
        self.__setup_ui()

        # Connections
        self.__dataset_loader_button.clicked.connect(self.__load_predefined_dataset)

    def sizeHint(self) -> "QSize":
        return QSize(500, 300)

    def __setup_ui(self):
        splitter = QSplitter()

        # Set label names
        self.__options_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        self.__options_layout.addRow("Dataset name", self.__dataset_name_label)
        self.__options_layout.addRow("Total items (train)", self.__train_len_label)
        self.__options_layout.addRow("Total items (test)", self.__test_len_label)
        self.__options_layout.addRow(
            "Load predefined dataset", self.__dataset_loader_button
        )

        options_widget = QWidget()
        options_widget.setLayout(self.__options_layout)

        splitter.addWidget(options_widget)
        splitter.addWidget(self.__train_test_tabs)

        self.__main_layout.addWidget(splitter, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)

    def __load_predefined_dataset(self):
        datasets_loader_dialog = PredefinedDatasetsList.Dialog()

        accepted = datasets_loader_dialog.exec()

        if accepted:
            dataset_loader = datasets_loader_dialog.selected_loader()

            train, test = dataset_loader.load()

            self.__train_test_tabs.set_train_dataset(train)
            self.__train_test_tabs.set_test_dataset(test)

            self.__dataset_name_label.setText(dataset_loader.name)
            self.__train_len_label.setText(str(len(train)))
            self.__test_len_label.setText(str(len(test)))
