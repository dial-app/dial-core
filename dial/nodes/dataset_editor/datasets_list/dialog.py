# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Optional

from PySide2.QtCore import Slot
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from dial.base.datasets import DatasetLoader
    from .model import DatasetsListModel
    from .view import DatasetsListView
    from PySide2.QtWidgets import QWidget


class DatasetsListDialog(QDialog):
    """
    Dialog window for selecting between predefined datasets.
    """

    def __init__(
        self,
        model: "DatasetsListModel",
        view: "DatasetsListView",
        parent: "QWidget" = None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Datasets")

        # Attributes
        self.__dataset_loader: Optional["DatasetLoader"] = None

        # Setup MVC
        self.__model = model
        self.__model.setParent(self)
        self.__view = view
        self.__view.setParent(self)

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

        self.__view.activated.connect(self.__selected_loader_changed)

    def selected_loader(self) -> Optional["DatasetLoader"]:
        """
        Return the loaded currently selected by the Dialog.
        """
        return self.__dataset_loader

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

    @Slot("QModelIndex")
    def __selected_loader_changed(self, index: "QModelIndex"):
        """
        Slot called when a user clicks on any list item.
        """
        self.__dataset_loader = index.internalPointer()

        self.__update_description(self.__dataset_loader)

    @Slot("DatasetLoader")
    def __update_description(self, dataset: "DatasetLoader"):
        """
        Update the description on the right widget after selecting a new dataset.
        """
        self.__name_label.setText(dataset.name)
        self.__brief_label.setText(dataset.brief)
        self.__types_label.setText(
            ", ".join([str(dataset.x_type), str(dataset.y_type)])
        )
