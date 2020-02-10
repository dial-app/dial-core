# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF
from PySide2.QtGui import QBrush, QColor, QPen
from PySide2.QtWidgets import QGraphicsItem


class GraphicsSocket(QGraphicsItem):
    def __init__(self, socket, parent=None):
        super().__init__(parent)

        self.socket = socket

        self.radius = 7.0

        self.outline_pen = QPen(QColor("#FF002132"))
        self.outline_pen.setWidthF(2)

        self.background_brush = QBrush(QColor("#FFFFA637"))

    def boundingRect(self):
        return QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)

    def paint(self, painter, option, widget=None):

        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawEllipse(self.boundingRect())
