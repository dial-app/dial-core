# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QSize
from PySide2.QtWidgets import (
    QFormLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QWidget,
)

from dial.utils import log

from .dataset_table import TrainTestTable

LOGGER = log.get_logger(__name__)


class DatasetEditorWidget(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    # TODO: Change dataset_table_widget
    def __init__(self, dataset_table_widget=TrainTestTable.Widget(), parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__options_layout = QFormLayout()

        self.__train_test_tabs = dataset_table_widget
        self.__train_test_tabs.setParent(self)

        self.__dataset_name_label = QLabel("")
        self.__dataset_loader_button = QPushButton("More...")

        self.__train_len_label = QLabel("")
        self.__test_len_label = QLabel("")

        # Configure interface
        self.__setup_ui()

    def sizeHint(self):
        return QSize(600, 500)

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
