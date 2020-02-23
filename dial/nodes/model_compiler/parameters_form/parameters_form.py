# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt, Signal
from PySide2.QtWidgets import QComboBox, QFormLayout, QPushButton, QSpinBox, QWidget


class ParametersForm(QWidget):
    """
    Form for changing the parameters used for the training process.
    """

    epoch_value_changed = Signal(int)
    loss_function_changed = Signal(str)
    optimizer_changed = Signal(str)
    batch_size_changed = Signal(int)
    compile_model = Signal()

    def __init__(self, parent: "QWidget" = None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QFormLayout()

        self.__epoch_spinbox = QSpinBox()
        self.__epoch_spinbox.setMinimum(1)

        self.__loss_function_combobox = QComboBox()
        self.__loss_function_combobox.addItems(
            ["mean_squared_error", "binary_crossentropy", "categorical_crossentropy"]
        )

        self.__optimizer_combobox = QComboBox()
        self.__optimizer_combobox.addItems(["adam", "sgd", "rmsprop"])

        self.__batch_size_spinbox = QSpinBox()
        self.__batch_size_spinbox.setRange(1, 99999999)
        self.__batch_size_spinbox.setValue(32)

        self.__compile_button = QPushButton("Compile model")

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

        self.__batch_size_spinbox.valueChanged.connect(
            lambda value: self.batch_size_changed.emit(value)
        )

        self.__compile_button.clicked.connect(lambda: self.compile_model.emit())

    def __setup_ui(self):
        self.__main_layout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.__main_layout.setFormAlignment(Qt.AlignHCenter)
        self.__main_layout.setHorizontalSpacing(50)

        self.__main_layout.addRow("Epochs", self.__epoch_spinbox)
        self.__main_layout.addRow("Loss functions", self.__loss_function_combobox)
        self.__main_layout.addRow("Optimizers", self.__optimizer_combobox)
        self.__main_layout.addRow("Batch Size", self.__batch_size_spinbox)
        self.__main_layout.addWidget(self.__compile_button)

        self.setLayout(self.__main_layout)
