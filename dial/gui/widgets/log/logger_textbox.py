# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import logging

from PySide2.QtWidgets import QPlainTextEdit, QVBoxLayout, QWidget


class LoggerTextboxWidget(logging.Handler, QWidget):
    """The LoggerTextboxWidget class provides a textbox widget that can also work as a
    logging handler for the Python logging system.

    Examples:
        textbox_logger = LoggerTextboxWidget()
        logging.getLogger().addHandler(textbox_logger)
    """

    def __init__(self, formatter: "logging.Formatter", parent: QWidget = None):
        logging.Handler.__init__(self)
        QWidget.__init__(self, parent)

        self.setFormatter(formatter)

        self._textbox = QPlainTextEdit(self)

        self.__setup_ui()

    @property
    def text(self) -> str:
        """Returns the text written on the textbox."""
        return self._textbox.toPlainText()

    def set_plain_text(self, text: str):
        """Replaces the textbox content with `text`."""
        self._textbox.setPlainText(text)

    def emit(self, record):
        """This method is called each time a logger emits a message. It applies the
        corresponding format and sends it to the textbox."""
        msg = self.format(record)
        self._textbox.appendPlainText(msg)

    def __setup_ui(self):
        """Configures the widget and layout settings."""
        # Log messages window must be readonly
        self._textbox.setReadOnly(True)

        # Add log textbox to layout without margins
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self._textbox)

        self.setLayout(layout)
