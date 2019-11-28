# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dialog window for selecting between predefined datasets.
"""

from PySide2.QtCore import QModelIndex, Slot
from PySide2.QtWidgets import (QDialog, QDialogButtonBox, QFormLayout,
                               QHBoxLayout, QLabel, QVBoxLayout)

from tfg.utils import Tfg

from .model import PredefinedDatasetsListModel
from .view import PredefinedDatasetsListView


class PredefinedDatasetsDialog(QDialog):
    """
    Dialog window for selecting between predefined datasets.
    """

    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Predefined datasets")

        # Setup MVC
        self.__model = PredefinedDatasetsListModel(self)
        self.__view = PredefinedDatasetsListView(self)
        self.__view.setModel(self.__model)

        # Create widgets
        self.__name_label = QLabel()
        self.__brief_label = QLabel()
        self.__types_label = QLabel()

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create Layouts
        self.__main_layout = QHBoxLayout()
        self.__description_layout = QFormLayout()

        # Setup UI
        self.__setup_ui()

        self.__view.activated.connect(self.update_description)

    def __setup_ui(self):
        # Main layout
        self.setLayout(self.__main_layout)

        # Right side (Description)

        self.__description_layout.addRow("Name", self.__name_label)
        self.__description_layout.addRow("Brief", self.__brief_label)
        self.__description_layout.addRow("Data types:", self.__types_label)

        # Extra vertical layout for dialog button_box widget
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.__description_layout)
        right_layout.addWidget(self.button_box)

        # Add widgets to main layout
        self.__main_layout.addWidget(self.__view)
        self.__main_layout.addLayout(right_layout)

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
