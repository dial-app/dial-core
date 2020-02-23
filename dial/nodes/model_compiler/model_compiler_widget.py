# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtWidgets import QGridLayout, QWidget

from dial.utils import log

if TYPE_CHECKING:
    from .parameters_form import ParametersForm


LOGGER = log.get_logger(__name__)


class ModelCompilerWidget(QWidget):
    def __init__(self, parameters_form: "ParametersForm", parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__parameters_form = parameters_form

        # Configure interface
        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__parameters_form)

        self.setLayout(self.__main_layout)
