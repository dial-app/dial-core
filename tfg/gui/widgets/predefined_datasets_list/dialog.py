# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QModelIndex, Slot
from PySide2.QtWidgets import QDialog, QFormLayout, QHBoxLayout, QLabel

from tfg.utils import Tfg

from .model import PredefinedDatasetsListModel
from .view import PredefinedDatasetsListView


class PredefinedDatasetsDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Predefined datasets")

        # Setup MVC
        self.__model = PredefinedDatasetsListModel(self)
        self.__view = PredefinedDatasetsListView(self)
        self.__view.setModel(self.__model)

        self.__setup_ui()

        self.__view.activated.connect(self.update_description)

    def __setup_ui(self):
        # Main layout
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

        # Right widget (Description)
        self.__name_label = QLabel()
        self.__brief_label = QLabel()
        self.__types_label = QLabel()

        self.__form_layout = QFormLayout()

        self.__form_layout.addRow("Name", self.__name_label)
        self.__form_layout.addRow("Brief", self.__brief_label)
        self.__form_layout.addRow("Data types:", self.__types_label)

        # Add widgets to main layout
        self.__layout.addWidget(self.__view)
        self.__layout.addLayout(self.__form_layout)

    @Slot(QModelIndex)
    def update_description(self, index: QModelIndex):
        """
        Update the description on the right widget after selecting a new dataset.
        """
        dataset = index.data(Tfg.RawRole)

        self.__name_label.setText(dataset.name)
        self.__brief_label.setText(dataset.brief)
        self.__types_label.setText(
            ", ".join([dataset.x_type.name, dataset.y_type.name])
        )
