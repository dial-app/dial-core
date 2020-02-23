# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import logging
from typing import TYPE_CHECKING

from PySide2.QtCore import QSize
from PySide2.QtWidgets import QDialog, QVBoxLayout

if TYPE_CHECKING:
    from .logger_textbox import LoggerTextboxWidget
    from PySide2.QtWidgets import QWidget


class LoggerDialog(QDialog):
    """The LoggerDialog class provides a dialog window prepared for displaying messages
    from the Python logging system.

    Examples:
        logger_dialog = LoggerDialog()
        logging.getLogger().addHandler(logger_dialog.handler)
    """

    def __init__(self, textbox_widget: "LoggerTextboxWidget", parent: "QWidget" = None):
        super().__init__(parent)

        self.textbox = textbox_widget
        self.textbox.setParent(self)

        self.__setup_ui()

    def handler(self) -> "logging.Handler":
        """Returns a logging handler associated to this dialog. Must be used to send log
        messages to it.
        """
        return self.textbox

    def sizeHint(self) -> "QSize":
        """Preferred size of this dialog."""
        return QSize(800, 600)

    def __setup_ui(self):
        """Configures the widget and layout settings."""

        self.setWindowTitle("Logging window")

        layout = QVBoxLayout()
        layout.addWidget(self.textbox)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
