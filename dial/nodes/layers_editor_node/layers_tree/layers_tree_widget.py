# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtWidgets import QVBoxLayout, QWidget


class LayersTreeWidget(QWidget):
    """
    Widget for displaying the list of avaliable layers for constructing models.
    """

    def __init__(self, layerstree_factory, parent=None):
        super().__init__(parent)

        self.__model = layerstree_factory.Model(parent=self)
        self.__view = layerstree_factory.View(parent=self)
        self.__view.setModel(self.__model)

        self.__main_layout = QVBoxLayout()

        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__view)

        self.setLayout(self.__main_layout)

    def set_model(self, model):
        """
        """
        self.__model.load_model(model)