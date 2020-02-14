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

        # Connection can be selectable
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # TODO: Track start and end ports

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
        return self.__start

    @start.setter
    def start(self, position: QPointF):
        self.__start = position
        self.__start_graphics_port = None
        self.updatePath()

    @property
    def end(self):
        """Returns the end position of the connection."""
        return self.__end

    @end.setter
    def end(self, position: QPointF):
        self.__end = position
        self.__end_graphics_port = None
        self.updatePath()

    @property
    def start_graphics_port(self):
        return self.__start_graphics_port

    @start_graphics_port.setter
    def start_graphics_port(self, port: GraphicsPort):
        self.__start_graphics_port = port
        self.__start = port.graphics_node.pos() + port.pos()
        self.color = port.color
        self.updatePath()

    @property
    def end_graphics_port(self):
        return self.__end_graphics_port

    @end_graphics_port.setter
    def end_graphics_port(self, port: GraphicsPort):
        self.__end_graphics_port = port
        self.__end = port.graphics_node.pos() + port.pos()
        self.updatePath()

    def updatePath(self):
        path = QPainterPath(self.start)
        path.lineTo(self.end)

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
