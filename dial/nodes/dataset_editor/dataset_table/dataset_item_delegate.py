# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from typing import TYPE_CHECKING

import qimage2ndarray
from PySide2.QtCore import QRect, QSize, Qt
from PySide2.QtGui import QPixmap, QPixmapCache
from PySide2.QtWidgets import QStyledItemDelegate

from dial.base.datasets import datatype
from dial.utils import Dial

if TYPE_CHECKING:
    from PySide2.QtCore import QModelIndex
    from PySide2.QtGui import QPainter
    from PySide2.QtWidgets import QStyleOptionViewItem
    from PySide2.QtWidgets import QObject


class DatasetItemDelegate(QStyledItemDelegate):
    """
    Delegate that knows how to paint any data that can be loaded to a dataset.
    """

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.min_image_size = QSize(100, 100)

    def paint(
        self, painter: "QPainter", option: "QStyleOptionViewItem", index: "QModelIndex"
    ):
        """
        Paint the element according to its type.
        """
        # Get the data type (Image, Numeric...)
        data_type = index.data(Dial.TypeRole.value)

        # Draw image
        if isinstance(data_type, datatype.ImageArray):
            self.__paint_pixmap(painter, option, index)

        # Draw anything else as a string
        else:
            self.__paint_string(painter, option, index)

    def __paint_pixmap(
        self, painter: "QPainter", option: "QStyleOptionViewItem", index: "QModelIndex"
    ):
        """
        Paint a pixmap centered on the cell.
        Generated pixmaps are saved on cache by the name "dataset_row_col"
        """

        raw_data = index.internalPointer()

        # Load Qt pixap from array
        pix = QPixmap()
        pix_name = str(id(raw_data))

        if not QPixmapCache.find(pix_name, pix):
            # Get image raw array

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

    def __paint_string(
        self, painter: "QPainter", option: "QStyleOptionViewItem", index: "QModelIndex"
    ):
        """
        Paint a value that can be converted to string.
        """

        # Get numeric raw value as a string
        display_text = index.data(Qt.DisplayRole)

        alignment = Qt.AlignCenter

        # Get the datatype
        data_type = index.data(Dial.TypeRole.value)

        # Align arrays to left
        if isinstance(data_type, datatype.NumericArray):
            alignment = Qt.AlignLeft

        # Paint it
        painter.drawText(option.rect, alignment, display_text)

    def sizeHint(self, option: "QStyleOptionViewItem", index: "QModelIndex"):
        """
        Return the size needed by the delegate to display its contents.
        """

        return self.min_image_size
