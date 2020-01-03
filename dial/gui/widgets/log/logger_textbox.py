# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widget used for displaying the outputs of a Python logger onto a plain text widget.
"""

import logging

from dial.utils import log
from PySide2.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget


class LoggerTextboxWidget(logging.Handler, QWidget):
    """
    Widget used for displaying the outputs of a Python logger onto a plain text widget.
    """

    def __init__(self, parent=None):
        logging.Handler.__init__(self)
        QWidget.__init__(self, parent)

        self.setFormatter(log.FORMATTER)

        self._textbox = QPlainTextEdit(self)

        self._setup()

    def _setup(self):
        """
        Setup the widget settings and layout configuration.
        """

        self._textbox.setReadOnly(True)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._textbox)

        self.setLayout(layout)

    def set_plain_text(self, text: str):
        """
        Set new Plain Text on the textbox.
        """
        self._textbox.setPlainText(text)

    def emit(self, record):
        """
        This method is called each time a logger emits a message. Apply the
        corresponding format and send to the textbox.
        """

        msg = self.format(record)
        self._textbox.appendPlainText(msg)
