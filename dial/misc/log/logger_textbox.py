# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widget used for displaying the outputs of a Python logger onto a plain text widget.
"""

import logging

from PySide2.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget

from dial.utils import log


class LoggerTextboxWidget(logging.Handler, QWidget):
    """
    Widget used for displaying the outputs of a Python logger onto a plain text widget.
    """

    def __init__(self, parent=None):
        logging.Handler.__init__(self)
        QWidget.__init__(self, parent)

        self.setFormatter(log.FORMATTER)

        self._textbox = QPlainTextEdit(self)

        self.__setup_ui()

    def __setup_ui(self):
        """
        Setup the widget settings and layout configuration.
        """

        # Log messages window must be readonly
        self._textbox.setReadOnly(True)

        # Add log textbox to layout without margins
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._textbox)

        self.setLayout(layout)

    @property
    def text(self) -> str:
        """
        Return the text content of the logger window.
        """
        return self._textbox.toPlainText()

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
