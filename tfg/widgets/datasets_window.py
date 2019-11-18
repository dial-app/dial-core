# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtWidgets import QPushButton, QSpacerItem, QVBoxLayout, QWidget


class DatasetsWindow(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._main_layout = QVBoxLayout(self)

        self._setup()

    def _setup(self):
        self._main_layout.addWidget(QPushButton("Test"))  # TODO: Remove later
        self._main_layout.addSpacing(400)

        self.setLayout(self._main_layout)
