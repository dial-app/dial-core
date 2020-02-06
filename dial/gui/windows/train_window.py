# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

import sys

from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import (
    QHBoxLayout,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EmittingStream(QObject):
    text_written = Signal(str)

    def write(self, text: str):
        self.text_written.emit(text)

    def flush(self):
        pass


class TrainWindow(QWidget):
    """
    """

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__main_layout = QVBoxLayout()

        self.__start_train_button = QPushButton("Start training")
        self.__stop_train_button = QPushButton("Stop training")

        self.__training_output_textbox = QPlainTextEdit()

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__start_train_button.clicked.connect(
            lambda: self.__project_manager.start_training_model()
        )

        self.__start_train_button.clicked.connect(
            lambda: self.__training_output_textbox.clear()
        )

        self.__stop_train_button.clicked.connect(
            lambda: self.__project_manager.stop_training_model()
        )

        stream = EmittingStream()
        stream.text_written.connect(self.write_training_output)

        sys.stdout = stream

    @Slot(str)
    def write_training_output(self, text):
        self.__training_output_textbox.appendPlainText(text)

    def __setup_ui(self):
        self.setLayout(self.__main_layout)

        self.__stop_train_button.setEnabled(False)

        self.__training_output_textbox.setReadOnly(True)

        hbox_layout = QHBoxLayout()
        hbox_layout.addWidget(self.__start_train_button)
        hbox_layout.addWidget(self.__stop_train_button)

        self.__main_layout.addLayout(hbox_layout)
        self.__main_layout.addWidget(self.__training_output_textbox)
