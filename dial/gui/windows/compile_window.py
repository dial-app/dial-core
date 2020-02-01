# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Window for all the parameters and compilation options (loss functions, epochs...)
"""

from PySide2.QtWidgets import QGridLayout, QWidget


class CompileWindow(QWidget):
    """
    Window for all the dataset related operations (Visualization, loading...)
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialize widgets
        self.__main_layout = QGridLayout()

        # Configure interface
        self.__setup_ui()

        # Connect signals

    def __setup_ui(self):
        self.__main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.__main_layout)
