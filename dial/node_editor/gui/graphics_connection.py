# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QPointF
from PySide2.QtGui import QPainter, QPainterPath, QPainterPathStroker, QPen
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)


class GraphicsConnection(QGraphicsPathItem):
    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)

        # Connection can be selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # TODO: Track start and end ports

        self.__start = QPointF(0, 0)
        self.__end = QPointF(0, 0)

        # Colors/Pens/Brushes
        self.default_pen = QPen("#001000")
        self.default_pen.setWidthF(4)

        self.selected_pen = QPen("#00AA00")
        self.selected_pen.setWidthF(4)

        # Draw connections always on bottom
        self.setZValue(-1)

    @property
    def start(self):
        """Returns the start position of the connection."""
        return self.__start

    @start.setter
    def start(self, point: QPointF):
        """Sets a new start point for the connection."""
        self.__start = point
        print("New start point")

    @property
    def end(self):
        """Returns the end position of the connection."""
        return self.__end

    @end.setter
    def end(self, point: QPointF):
        """Sets a new end point for the connection."""
        self.__end = point
        print("New end point")

    def shape(self):
        """Returns a detailed shape of the connection."""
        stroker = QPainterPathStroker()
        stroker.setWidth(self.default_pen.widthF() * 4)

        path = QPainterPath(self.start)
        path.lineTo(self.end)

        return stroker.createStroke(path)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget = None,
    ):
        """Paint the connection as a line between the start and end points."""
        path = QPainterPath(self.start)
        path.lineTo(self.end)

        painter.setPen(self.default_pen if not self.isSelected() else self.selected_pen)
        painter.drawPath(path)
