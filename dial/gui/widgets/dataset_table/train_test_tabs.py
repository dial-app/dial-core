# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from dial.datasets import Dataset
from dial.gui.widgets.dataset_table import DatasetTableModel, DatasetTableView
from PySide2.QtWidgets import QTabWidget


class TrainTestTabs(QTabWidget):
    """
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.__train_model = DatasetTableModel(self)
        self.__train_view = DatasetTableView(self)
        self.__train_view.setModel(self.__train_model)

        self.__test_model = DatasetTableModel(self)
        self.__test_view = DatasetTableView(self)
        self.__test_view.setModel(self.__test_model)

        self.__setup_ui()

    def set_train_dataset(self, train_dataset: Dataset):
        """
        """
        self.__train_model.load_dataset(train_dataset)

    def set_test_dataset(self, test_dataset: Dataset):
        """
        """
        self.__test_model.load_dataset(test_dataset)

    def __setup_ui(self):
        self.addTab(self.__train_view, "Train")
        self.addTab(self.__test_view, "Test")
