# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Delegate that knows how to paint any data that can be loaded to a dataset.
"""

import qimage2ndarray
from PySide2.QtCore import QModelIndex, QRect, QSize, Qt
from PySide2.QtGui import QPainter, QPixmap, QPixmapCache
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from dial.datasets import DataType
from dial.utils import Dial


class DatasetItemDelegate(QStyledItemDelegate):
    """
    Delegate that knows how to paint any data that can be loaded to a dataset.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.min_image_size = QSize(100, 100)

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        """
        Paint the element according to its type.
        """
        # Get the data type (Image, Numeric...)
        data_type = index.data(Dial.TypeRole)

        # Draw image
        if data_type == DataType.ImageArray:
            self.__paint_pixmap(painter, option, index)

        # Draw anything else
        else:
            self.__paint_numeric(painter, option, index)

    def __paint_pixmap(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        """
        Paint a pixmap centered on the cell.
        Generated pixmaps are saved on cache by the name "dataset_row_col"
        """

        # Load Qt pixap from array
        pix = QPixmap()
        pix_name = f"{id(self)}_{index.row()}_{index.column()}"

        if not QPixmapCache.find(pix_name, pix):
            # Get image raw array
            raw_data = index.data(Dial.RawRole)

            # Load pix from raw array
            pix = QPixmap.fromImage(qimage2ndarray.array2qimage(raw_data))

            # Save pix on cache
            QPixmapCache.insert(pix_name, pix)

        pix = pix.scaled(option.rect.width(), option.rect.height(), Qt.KeepAspectRatio)

        # Calculate central position
        x_coord = option.rect.center().x() - pix.width() / 2
        y_coord = option.rect.center().y() - pix.height() / 2

        draw_rect = QRect(x_coord, y_coord, pix.width(), pix.height())

        # Draw pixm
        painter.drawPixmap(draw_rect, pix)

    def __paint_numeric(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        """
        Paint a numeric value centered on the cell.
        """

        # Get numeric raw value
        display_text = index.data(Qt.DisplayRole)

        # Paint it
        painter.drawText(option.rect, Qt.AlignCenter, display_text)

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Return the size needed by the delegate to display its contents.
        """

        return self.min_image_size
