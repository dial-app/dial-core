# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRect
from PySide2.QtWidgets import (
    QGraphicsProxyWidget,
    QLabel,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class NodeContentWidget(QGraphicsProxyWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.widget_label = QLabel("Some Title")
        self.text_edit = QTextEdit("foo")
        self.layout = QVBoxLayout()

        self.__setup_ui()

    def __setup_ui(self):
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(self.text_edit)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)

        self.setWidget(self.main_widget)
