# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Loggers used to display information and debug."""

import logging
from io import StringIO

from PySide2.QtWidgets import QDialog, QPlainTextEdit, QVBoxLayout, QWidget

logging.basicConfig(level=logging.DEBUG)

mainwindow = logging.getLogger("mainwindow")


class LoggerTextboxWidget(logging.Handler, QWidget):
    """
    Widget used for displaying the outputs of a Python logger onto a plain text widget.
    """

    def __init__(self, parent):
        logging.Handler.__init__(self)
        QWidget.__init__(self, parent)

        self._textbox = QPlainTextEdit(self)

        self._setup()

        self._add_logging_handlers()

    def _setup(self):
        """
        Setup the widget settings and layout configuration.
        """

        self._textbox.setReadOnly(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._textbox)

        self.setLayout(layout)

    def emit(self, record):
        """
        This method is called each time a logger emits a message. Apply the
        corresponding format and send to the textbox.
        """

        msg = self.format(record)
        self._textbox.appendPlainText(msg)

    def _add_logging_handlers(self):
        """
        Add all loggers which contents should be displayed by this widget.
        """

        mainwindow.addHandler(self)


class LoggerTextboxDialog(QDialog):
    """
    Pop-up window displaying the LoggerTextbox widget.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self._logger_textbox = LoggerTextboxWidget(self)

        self._setup()

    def _setup(self):
        """
        Setup the widget settings and layout configuration.
        """

        self.setWindowTitle("Log")

        layout = QVBoxLayout()
        layout.addWidget(self._logger_textbox)

        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)
