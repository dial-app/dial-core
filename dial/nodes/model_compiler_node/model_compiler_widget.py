# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the model related operations (Create/Modify NN architectures)
"""

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGridLayout, QMainWindow, QWidget

from dial.utils import log

from .parameters_form import ParametersFormFactory

LOGGER = log.get_logger(__name__)


class ModelCompilerWidget(QWidget):
    """
    """

    def __init__(self, parameters_form, parent: QWidget = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()
        self.__parameters_form = parameters_form

        # Configure interface
        self.__setup_ui()

    def __setup_ui(self):
        self.__main_layout.setContentsMargins(100, 100, 100, 100)

        self.__main_layout.addWidget(self.__parameters_form)

        self.setLayout(self.__main_layout)
