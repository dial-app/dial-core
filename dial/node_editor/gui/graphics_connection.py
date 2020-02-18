# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QColor, QPainter, QPainterPath, QPen
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsPathItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from .graphics_port import GraphicsPort


class GraphicsConnection(QGraphicsPathItem):
    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)

        # A Connection can be selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        self.__start = QPointF(0, 0)
        self.__end = QPointF(0, 0)

        self.__start_graphics_port: Optional[GraphicsPort] = None
        self.__end_graphics_port: Optional[GraphicsPort] = None

        # Colors/Pens/Brushes
        self.__color = QColor("black")

        self.__default_pen = QPen(self.color)
        self.__default_pen.setWidthF(4.0)

        # Draw connections always on bottom
        self.setZValue(-1)

        self.update()

    @property
    def color(self):
        """Returns the color of the connection."""
        return self.__color

    @color.setter
    def color(self, color: QColor):
        """Sets a new color for the connection, updating the QPen used for paintingg"""
        self.__color = color
        self.__default_pen.setColor(self.__color)

    @property
    def start(self):
        """Returns the start position of the connection."""
        return (
            self.__start
            if not self.__start_graphics_port
            else self.__start_graphics_port.pos()
        )

    @start.setter
    def start(self, position: QPointF):
        self.__start = position

        if self.__start_graphics_port:
            self.__start_graphics_port.remove_connection(self)
        self.__start_graphics_port = None
        self.updatePath()

    @property
    def end(self):
        """Returns the end position of the connection."""
        return (
            self.__end
            if not self.__end_graphics_port
            else self.__end_graphics_port.pos()
        )

    @end.setter
    def end(self, position: QPointF):
        self.__end = position

        if self.__end_graphics_port:
            self.__end_graphics_port.remove_connection(self)
        self.__end_graphics_port = None
        self.updatePath()

    @property
    def start_graphics_port(self):
        return self.__start_graphics_port

    @start_graphics_port.setter
    def start_graphics_port(self, port: GraphicsPort):
        # Updates the start position
        self.__start = port.pos()

        # Assigns a new start port
        self.__start_graphics_port = port
        self.__start_graphics_port.add_connection(self)

        # The connection adopts the color of the port
        self.color = port.color

        self.updatePath()

    @property
    def end_graphics_port(self):
        return self.__end_graphics_port

    @end_graphics_port.setter
    def end_graphics_port(self, port: GraphicsPort):
        # Updates the end position
        self.__end = port.pos()

        # Assigns a new end port
        self.__end_graphics_port = port
        self.__end_graphics_port.add_connection(self)

        self.updatePath()

    def updatePath(self):
        """Create a new path from the start and end points of the line."""
        path = QPainterPath(self.start)

        diffx = self.end.x() - self.start.x()

        c0x = self.start.x() + (diffx / 3)
        c0y = self.start.y()
        c1x = self.end.x() - (diffx / 3)
        c1y = self.end.y()

        path.cubicTo(c0x, c0y, c1x, c1y, self.end.x(), self.end.y())

        self.setPath(path)
        self.update()

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange:
            self.pen().setColor(self.color if value else self.color.lighter(200))

        return super().itemChange(change, value)

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget = None,
    ):
        """Paint the connection as a line between the start and end points."""
        painter.setPen(self.__default_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())
