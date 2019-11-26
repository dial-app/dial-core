# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import qimage2ndarray
from PySide2.QtCore import QModelIndex, QRect, QSize, Qt
from PySide2.QtGui import QPainter, QPixmap
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from tfg.datasets import DataType
from tfg.utils import Tfg


class DatasetItemDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.min_image_size = QSize(100, 100)

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        # Get the data type (Image, Numeric...)
        data_type = index.data(Tfg.TypeRole)
        raw_data = index.data(Tfg.RawRole)

        # Draw image
        if data_type == DataType.ImageArray:
            # Load Qt pixmap from array
            pixmap = QPixmap.fromImage(qimage2ndarray.array2qimage(raw_data))
            pixmap = pixmap.scaled(
                option.rect.width(), option.rect.height(), Qt.KeepAspectRatio
            )

            # Calculate central position
            x_coord = option.rect.center().x() - pixmap.width() / 2
            y_coord = option.rect.center().y() - pixmap.height() / 2

            draw_rect = QRect(x_coord, y_coord, pixmap.width(), pixmap.height())

            # Draw pixmap
            painter.drawPixmap(draw_rect, pixmap)

        # Draw anything else
        else:
            painter.drawText(option.rect, Qt.AlignCenter, f"{raw_data}")

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Return the size needed by the delegate to display its contents.
        """
        return self.min_image_size
