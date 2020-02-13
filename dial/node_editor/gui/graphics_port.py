# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF
from PySide2.QtGui import QBrush, QPen
from PySide2.QtWidgets import QGraphicsItem

from .type_colors import TypeColor


class GraphicsPort(QGraphicsItem):
    def __init__(self, port, parent=None):
        super().__init__(parent)

        self.__port = port

        self.radius = 8

        # Colors/Pens/Brushes
        port_color = TypeColor.get_color_for(port.port_type)

        self.outline_pen = QPen(port_color.darker())
        self.outline_pen.setWidthF(2)
        self.background_brush = QBrush(port_color)

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawEllipse(self.boundingRect())
