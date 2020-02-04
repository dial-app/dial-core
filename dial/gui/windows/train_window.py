# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtWidgets import QPushButton, QVBoxLayout, QWidget


class TrainWindow(QWidget):
    """
    """

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__main_layout = QVBoxLayout()

        self.__train_button = QPushButton("Start training")

        # Configure interface
        self.__setup_ui()

        # Connect signals
        self.__train_button.clicked.connect(
            lambda: self.__project_manager.train_model()
        )

    def __setup_ui(self):
        self.setLayout(self.__main_layout)

        self.__main_layout.addWidget(self.__train_button)
