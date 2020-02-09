# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QLineF, QPointF, QRectF, Qt
from PySide2.QtGui import QPainterPath, QPainterPathStroker, QPen
from PySide2.QtWidgets import QGraphicsItem


class Edge(QGraphicsItem):

    Type = QGraphicsItem.UserType + 1

    def __init__(self, parent=None):
        super().__init__(parent)

        self.start_point = QPointF()
        self.end_point = QPointF(250, 100)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def type(self):
        return Edge.Type

    def boundingRect(self):
        return QRectF(self.start_point, self.end_point).normalized()

    def shape(self):
        path = QPainterPath()
        path.lineTo(self.start_point)
        path.lineTo(self.end_point)

        path_stroker = QPainterPathStroker()
        path_stroker.setWidth(10)

        return path_stroker.createStroke(path)

    def paint(self, painter, option, widget):
        line = QLineF(self.start_point, self.end_point)

        line_pen = QPen(Qt.black, 3)

        painter.setPen(line_pen)

        painter.drawLine(line)

    def mouseMoveEvent(self, event):

        distance_to_start = QLineF(self.start_point, event.pos()).length()
        distance_to_end = QLineF(self.end_point, event.pos()).length()

        self.prepareGeometryChange()
        if distance_to_start < distance_to_end:
            self.start_point = event.pos()
        else:
            self.end_point = event.pos()

        # return super().mouseMoveEvent(event)
