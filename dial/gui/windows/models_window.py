# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the model related operations (Create/Modify NN architectures)
"""

from PySide2.QtWidgets import QGridLayout, QWidget
from tensorflow.keras.applications.vgg16 import VGG16

from dial.utils import log

LOGGER = log.get_logger(__name__)


class ModelsWindow(QWidget):
    """
    """

    def __init__(self, model_table, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__model_table = model_table

        self.__main_layout = QGridLayout()

        # Configure interface
        self.__setup_ui()

        # Connect signals

        # TODO: Remove from here
        self.__model_table.set_model(VGG16())

    def __setup_ui(self):
        self.__main_layout.addWidget(self.__model_table, 0, 0)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)
