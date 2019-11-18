# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widget for displaying some content example of the dataset.
"""

import matplotlib.pyplot as plt
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class DatasetView(QWidget):
    def __init__(self, dataset, parent):
        super().__init__(parent)

        self._dataset = dataset
        self._display_limit = 25  # Max nº of items to display

        self._setup()
        self._update_displayed_content()

    def _setup(self):
        layout = QVBoxLayout()

        self.setLayout(layout)

    def _update_displayed_content(self):
        # TODO: Manage other types of data
        # Display a batch of data from the train set

        for x, y in self._dataset.head(self._display_limit):
            hbox = QHBoxLayout()
            hbox.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

            qimage = QImage(x, x.shape[0], x.shape[1], QImage.Format_Grayscale8)
            label_display = QLabel()
            label_display.setPixmap(QPixmap(qimage))

            label_output = QLabel()
            label_output.setText(str(y))

            hbox.addWidget(label_display)
            hbox.addWidget(label_output)

            self.layout().addLayout(hbox)
