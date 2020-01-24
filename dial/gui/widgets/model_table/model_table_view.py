# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QAction, QHeaderView, QMenu, QTableView


class ModelTableView(QTableView):
    """
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Actions
        self.__hide_action = QAction("hue", self)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.horizontalHeader().setContextMenuPolicy(Qt.CustomContextMenu)
        self.horizontalHeader().customContextMenuRequested.connect(
            self.show_header_context_menu
        )

        self.__header_context_menu = None

    def setModel(self, model):
        # Assign model to view by calling the parent method
        super().setModel(model)

        # Additional: Create a context menu for showing/hiding the table headers
        # (columns)
        self.__header_context_menu = QMenu(self)
        header = self.horizontalHeader()

        # Iterate through each column
        for i in range(header.count()):
            column_label = model.headerData(
                section=i, orientation=Qt.Horizontal, role=Qt.DisplayRole
            )

            # Add a checkable action corresponding to each column
            action = self.__header_context_menu.addAction(column_label)
            action.setCheckable(True)
            action.setChecked(True)

            # Each action will show/hide the corresponding column referenced by its
            # index depending on if the action is checked or not (toggled)
            action.toggled.connect(
                lambda toggled, index=i: header.showSection(index)
                if toggled
                else header.hideSection(index)
            )

    def show_header_context_menu(self, point):
        if not self.__header_context_menu:
            return

        self.__header_context_menu.popup(self.horizontalHeader().mapToGlobal(point))
