# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QColor, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsPathItem


class GraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        # Appareance
        self.default_pen = QPen(QColor("#001000"))
        self.default_pen.setWidthF(3.0)
        self.selected_pen = QPen(QColor("#00FF00"))
        self.selected_pen.setWidthF(3.0)

        self.pos_source = QPointF(0, 0)
        self.pos_destination = QPointF(200, 100)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

    def paint(self, painter, option, widget=None):
        self.updatePath()

        self.setPen(self.default_pen if not self.isSelected() else self.selected_pen)
        self.setBrush(Qt.NoBrush)

        painter.drawPath(self.path())

    def boundingRect(self):
        return QRectF(
            self.pos_source.x(),
            self.pos_source.y(),
            self.pos_destination.x() - self.pos_source.x(),
            self.pos_destination.y() - self.pos_source.x(),
        )

    def updatePath(self):
        """Handles drawing QPainterPath from Point A to B"""
        raise NotImplementedError("This method needs to be overriden in a child class")


class GraphicsEdgeDirect(GraphicsEdge):
    def shape(self):
        path = QPainterPath(self.pos_source)
        path.lineTo(self.pos_destination)

        return path

    def updatePath(self):
        print("Updatepath")
        self.setPath(self.shape())


class GraphicsEdgeBezier(GraphicsEdge):
    def updatePath(self):
        s = self.pos_source
        d = self.pos_destination

        dist = (d.x() - s.x()) * 0.5
        if s.x() > d.x():  # Abs
            dist *= -1

        path = QPainterPath(self.pos_source)

        path.cubicTo(
            s.x() + dist,
            s.y(),
            d.x() - dist,
            d.y(),
            self.pos_destination.x(),
            self.pos_destination.y(),
        )

        self.setPath(path)
