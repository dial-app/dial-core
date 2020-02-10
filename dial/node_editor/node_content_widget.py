# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QLabel, QTextEdit, QVBoxLayout, QWidget


class NodeContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__setup_ui()

    def __setup_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.widget_label = QLabel("Some Title")
        self.layout.addWidget(self.widget_label)
        self.layout.addWidget(QTextEdit("foo"))
