# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import QColor, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsPathItem


class GraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge

        # Appareance
        self.__color = QColor("#001000")
        self.default_pen = QPen(self.__color)
        self.default_pen.setWidthF(3.0)

        self.selected_pen = QPen(QColor("#00FF00"))
        self.selected_pen.setWidthF(3.0)

        self.dragging_pen = QPen(self.__color)
        self.dragging_pen.setWidthF(3.0)
        self.dragging_pen.setStyle(Qt.DashLine)

        self.pos_source = QPointF(0, 0)
        self.pos_destination = QPointF(200, 100)

        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.setZValue(-1)

        self.updatePositions()

    def set_source(self, x, y):
        self.pos_source = QPointF(x, y)

    def set_destination(self, x, y):
        self.pos_destination = QPointF(x, y)

    def updatePositions(self):
        start_socket_pos = self.edge.start_socket.node.graphics_node.pos()
        start_socket_pos += self.edge.start_socket.graphics_socket.pos()

        self.set_source(start_socket_pos.x(), start_socket_pos.y())

        if self.edge.end_socket:
            end_socket_pos = self.edge.end_socket.node.graphics_node.pos()
            end_socket_pos += self.edge.end_socket.graphics_socket.pos()

            self.set_destination(end_socket_pos.x(), end_socket_pos.y())

        self.update()

    def paint(self, painter, option, widget=None):
        self.updatePath()

        if not self.edge.end_socket:
            painter.setPen(self.dragging_pen)
        else:
            painter.setPen(
                self.default_pen if not self.isSelected() else self.selected_pen
            )

        painter.setBrush(Qt.NoBrush)

        painter.drawPath(self.path())

    def updatePath(self):
        """Handles drawing QPainterPath from Point A to B"""
        raise NotImplementedError("This method needs to be overriden in a child class")


class GraphicsEdgeDirect(GraphicsEdge):
    def updatePath(self):
        path = QPainterPath(self.pos_source)
        path.lineTo(self.pos_destination)

        self.setPath(path)


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
