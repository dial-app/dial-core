# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtWidgets import QVBoxLayout, QWidget


class ModelTableWidget(QWidget):
    """
    Widget for displaying the model definition.
    """

    def __init__(self, modeltable_factory, parent=None):
        super().__init__(parent)

        self.__model = modeltable_factory.Model(parent=self)
        self.__view = modeltable_factory.View(parent=self)
        self.__view.setModel(self.__model)

        self.__layout = QVBoxLayout()

        self.__setup_ui()

    def __setup_ui(self):
        self.__layout.addWidget(self.__view)
