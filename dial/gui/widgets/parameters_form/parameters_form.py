# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Form for changing the parameters used for the training process.
"""

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QComboBox, QFormLayout, QSpinBox, QWidget


class ParametersForm(QWidget):
    epoch_value_changed = Signal(int)
    loss_function_changed = Signal(str)
    optimizer_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QFormLayout()

        self.__epoch_spinbox = QSpinBox()
        self.__epoch_spinbox.setMinimum(1)

        self.__loss_function_combobox = QComboBox()
        self.__loss_function_combobox.addItems(
            ["mean_squared_error", "binary_crossentrompy"]
        )

        self.__optimizer_combobox = QComboBox()
        self.__optimizer_combobox.addItems(["adam", "sgd"])

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__epoch_spinbox.valueChanged.connect(
            lambda value: self.epoch_value_changed.emit(value)
        )

        self.__loss_function_combobox.currentIndexChanged[str].connect(
            lambda value: self.loss_function_changed.emit(value)
        )

        self.__optimizer_combobox.currentIndexChanged[str].connect(
            lambda value: self.optimizer_changed.emit(value)
        )

    def __setup_ui(self):
        self.__main_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.__main_layout.setFormAlignment(Qt.AlignHCenter)
        self.__main_layout.setHorizontalSpacing(200)

        self.__main_layout.addRow("Epochs", self.__epoch_spinbox)
        self.__main_layout.addRow("Loss functions", self.__loss_function_combobox)
        self.__main_layout.addRow("Optimizers", self.__optimizer_combobox)

        self.setLayout(self.__main_layout)
