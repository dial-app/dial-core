# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Pop-up window displaying the LoggerTextbox widget.
"""

import logging

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QVBoxLayout

from .logger_textbox import LoggerTextboxWidget


class LoggerDialog(QDialog):
    """
    Pop-up window displaying the LoggerTextbox widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.textbox = LoggerTextboxWidget(self)

        self.__setup_ui()

    def handler(self) -> logging.Handler:
        """
        Return log handler associated to this dialog (And used to write on it).
        """

        return self.textbox

    def sizeHint(self):
        return QSize(800, 600)

    def __setup_ui(self):
        """
        Setup the widget settings and layout configuration.
        """

        self.setWindowTitle("Log")

        layout = QVBoxLayout()

        layout.addWidget(self.textbox)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
