# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
"""

from PySide2.QtWidgets import QGridLayout, QWidget


class TrainWindow(QWidget):
    """
    """

    def __init__(self, project_manager, parent=None):
        super().__init__(parent)

        # Initialize components
        self.__project_manager = project_manager

        # Initialize widgets
        self.__main_layout = QGridLayout()

        # Configure interface
        self.__setup_ui()

    def __setup_ui(self):
        self.setLayout(self.__main_layout)
