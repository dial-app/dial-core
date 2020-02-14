# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF
from PySide2.QtGui import QBrush, QColor, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from .type_colors import TypeColor


class GraphicsPort(QGraphicsItem):
    def __init__(self, port, parent=None):
        super().__init__(parent)

        self.__port = port
        self.__port.graphics_port = self  # Add an instance reference to self

        self.graphics_node = parent

        self.radius = 8

        # Colors/Pens/Brushes
        self.__color = TypeColor.get_color_for(port.port_type)

        self.outline_pen = QPen(self.__color.darker())
        self.outline_pen.setWidthF(2)
        self.background_brush = QBrush(self.__color)

    @property
    def color(self) -> QColor:
        """Returns the color of the port."""
        return self.__color

    def boundingRect(self) -> QRectF:
        """Returns the bounding rect of the port."""
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget = None,
    ):
        """Paints the port."""
        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawEllipse(self.boundingRect())
