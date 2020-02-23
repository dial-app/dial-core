# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QVBoxLayout, QWidget

if TYPE_CHECKING:
    from .containers import ModelTableMVFactory


class ModelTableWidget(QWidget):
    """
    Widget for displaying the model definition.
    """

    def __init__(
        self, modeltable_mv_factory: "ModelTableMVFactory", parent: "QWidget" = None
    ):
        super().__init__(parent)

        self.__model = modeltable_mv_factory.Model(parent=self)
        self.__view = modeltable_mv_factory.View(parent=self)
        self.__view.setModel(self.__model)

        self.__main_layout = QVBoxLayout()

        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__view)

        self.setLayout(self.__main_layout)

    def set_model(self, model):
        self.__model.load_layers(model.layers)
