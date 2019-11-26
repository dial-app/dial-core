# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QDialog, QHBoxLayout

from .model import PredefinedDatasetsListModel
from .view import PredefinedDatasetsListView


class PredefinedDatasetsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Predefined datasets")

        self.__model = PredefinedDatasetsListModel(self)
        self.__view = PredefinedDatasetsListView(self)

        self.__view.setModel(self.__model)

        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__view)

        self.setLayout(self.__layout)
