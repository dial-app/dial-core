# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Pop-up window displaying the LoggerTextbox widget.
"""

from PySide2.QtWidgets import QDialog, QVBoxLayout

from .logger_textbox import LoggerTextboxWidget


class LoggerDialog(QDialog):
    """
    Pop-up window displaying the LoggerTextbox widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__logger_textbox = LoggerTextboxWidget(self)

        self.__setup_ui()

    def __setup_ui(self):
        """
        Setup the widget settings and layout configuration.
        """

        self.setWindowTitle("Log")

        layout = QVBoxLayout()

        layout.addWidget(self.__logger_textbox)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
