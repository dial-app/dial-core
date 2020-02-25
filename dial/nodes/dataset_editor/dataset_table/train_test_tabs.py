# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from dial.base.datasets import Dataset
    from PySide2.QtWidgets import QWidget
    from .containers import DatasetTableMVFactory


class TrainTestTabs(QTabWidget):
    """
    Widget for displaying the train/tests list. Each dataset is on its own tab on the
    widget.
    """

    def __init__(
        self, datasettable_mv_factory: "DatasetTableMVFactory", parent: "QWidget" = None
    ):
        super().__init__(parent)

        self.__train_model = datasettable_mv_factory.Model(parent=self)
        self.__train_view = datasettable_mv_factory.View(parent=self)
        self.__train_view.setModel(self.__train_model)

        self.__test_model = datasettable_mv_factory.Model(parent=self)
        self.__test_view = datasettable_mv_factory.View(parent=self)
        self.__test_view.setModel(self.__test_model)

        self.__setup_ui()

    def set_train_dataset(self, train_dataset: "Dataset"):
        """
        """
        self.__train_model.load_dataset(train_dataset)

    def set_test_dataset(self, test_dataset: "Dataset"):
        """
        """
        self.__test_model.load_dataset(test_dataset)

    def __setup_ui(self):
        self.addTab(self.__train_view, "Train")
        self.addTab(self.__test_view, "Test")
