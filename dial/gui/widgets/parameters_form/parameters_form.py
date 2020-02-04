# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Form for changing the parameters used for the training process.
"""

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QFormLayout, QSpinBox, QWidget


class ParametersForm(QWidget):
    epoch_value_changed = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QFormLayout()

        self.__epoch_spinbox = QSpinBox()

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__epoch_spinbox.valueChanged.connect(
            lambda value: self.epoch_value_changed.emit(value)
        )

    def __setup_ui(self):
        self.__main_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.__main_layout.setFormAlignment(Qt.AlignHCenter)
        self.__main_layout.setHorizontalSpacing(200)

        self.__main_layout.addRow("Epochs", self.__epoch_spinbox)

        self.setLayout(self.__main_layout)
