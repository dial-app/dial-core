# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widget for displaying some content example of the dataset.
"""

import matplotlib.pyplot as plt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class DatasetView(QWidget):
    def __init__(self, dataset, parent):
        super().__init__(parent)

        self._dataset = dataset
        self._display_limit = 10  # Max nº of items to display

        self._setup()
        self._update_displayed_content()

    def _setup(self):
        layout = QVBoxLayout()

        self.setLayout(layout)

    def _update_displayed_content(self):
        # TODO: Manage other types of data
        # Display a batch of data from the train set

        batch_x, batch_y = self._dataset[0]

        for i in range(min(self._display_limit, self._dataset.batch_size)):
            # TODO: Check number of channels on image
            hbox = QHBoxLayout()

            qimage = QImage(
                batch_x[i],
                batch_x[i].shape[0],
                batch_x[i].shape[1],
                QImage.Format_Grayscale8,
            )
            label_display = QLabel()
            label_display.setPixmap(QPixmap(qimage))

            label_output = QLabel()
            label_output.setText(str(batch_y[i]))

            hbox.addWidget(label_display)
            hbox.addWidget(label_output)

            self.layout().addLayout(hbox)
