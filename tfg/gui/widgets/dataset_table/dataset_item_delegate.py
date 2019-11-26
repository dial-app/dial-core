# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Delegate that knows how to paint any data that can be loaded to a dataset.
"""

import qimage2ndarray
from PySide2.QtCore import QModelIndex, QRect, QSize, Qt
from PySide2.QtGui import QPainter, QPixmap, QPixmapCache
from PySide2.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from tfg.datasets import DataType
from tfg.utils import Tfg


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
        data_type = index.data(Tfg.TypeRole)

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

        # Load Qt pixmap from array
        pixm = QPixmap()
        pixm_name = f"dataset_{index.row()}_{index.column()}"

        if not QPixmapCache.find(pixm_name, pixm):
            # Get image raw array
            raw_data = index.data(Tfg.RawRole)

            # Load pixm from raw array
            pixm = QPixmap.fromImage(qimage2ndarray.array2qimage(raw_data))

            # Save pixm on cache
            QPixmapCache.insert(pixm_name, pixm)

        pixm = pixm.scaled(
            option.rect.width(), option.rect.height(), Qt.KeepAspectRatio
        )

        # Calculate central position
        x_coord = option.rect.center().x() - pixm.width() / 2
        y_coord = option.rect.center().y() - pixm.height() / 2

        draw_rect = QRect(x_coord, y_coord, pixm.width(), pixm.height())

        # Draw pixm
        painter.drawPixmap(draw_rect, pixm)

    def __paint_numeric(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        """
        Paint a numeric value centered on the cell.
        """

        # Get numeric raw value
        raw_data = index.data(Tfg.RawRole)

        # Paint it
        painter.drawText(option.rect, Qt.AlignCenter, f"{raw_data}")

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        """
        Return the size needed by the delegate to display its contents.
        """

        return self.min_image_size
