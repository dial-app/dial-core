# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QSize, Qt
from PySide2.QtWidgets import QDialog, QGridLayout, QLabel, QListWidget


class LoadDatasetDialog(QListWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("List of built-in datasets")

        self._datasets_list = QListWidget(self)
        self._layout = QGridLayout()
        self._layout.setColumnStretch(0, 45)
        self._layout.setColumnStretch(1, 55)

        self._setup()

    def _setup(self):
        self._layout.addWidget(QLabel("Datasets:"), 0, 0)
        self._layout.addWidget(self._datasets_list, 1, 0)

        self.setLayout(self._layout)

    def sizeHint(self):
        return QSize(375, 400)
