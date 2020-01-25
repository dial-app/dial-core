# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dialog window for selecting between predefined datasets.
"""

from typing import Optional

from dial.misc import Dial
from PySide2.QtCore import QModelIndex, Slot
from PySide2.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from .model import ModelsListModel
from .view import ModelsListView


class ModelsListDialog(QDialog):
    """
    Dialog window for selecting between different models.
    """

    def __init__(
        self, model: ModelsListModel, view: ModelsListView, parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle("Models")

        # Attributes
        self.__model_loader = None

        # Setup MVC
        self.__model = model
        self.__model.setParent(self)
        self.__view = view
        self.__view.setParent(self)

        self.__view.setModel(self.__model)

        # Create widgets
        self.__name_label = QLabel()

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

    def selected_loader(self):
        """
        Return the loader currently selected by the Dialog.
        """
        return self.__model_loader

    def __setup_ui(self):
        # Main layout
        self.setLayout(self.__main_layout)

        # Right side (Description)
        self.__description_layout.addRow("Name", self.__name_label)

        # Extra vertical layout for dialog button_box widget
        right_layout = QVBoxLayout()
        right_layout.addLayout(self.__description_layout)
        right_layout.addWidget(self.button_box)

        # Add widgets to main layout
        self.__main_layout.addWidget(self.__view)
        self.__main_layout.addLayout(right_layout)

    @Slot(QModelIndex)
    def __selected_loader_changed(self, index: QModelIndex):
        """
        Slot called when a user clicks on any list item.
        """
        self.__model_loader = index.data(Dial.RawRole)

        self.__update_description(self.__model_loader)

    # @Slot(DatasetLoader)
    def __update_description(self, model_loader):
        """
        Update the description on the right widget after selecting a new dataset.
        """
        self.__name_label.setText(model_loader.name)
