# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# type: ignore

from typing import List

from PySide2.QtCore import QPointF, QRectF
from PySide2.QtGui import QBrush, QColor, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from .type_colors import TypeColor


class GraphicsPort(QGraphicsItem):
    def __init__(self, port, parent=None):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        self.graphics_node = parent

        self.__port = port
        self.__port.graphics_port = self  # Add an instance reference to self

        self.__connections = set()

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

    @property
    def connections(self) -> List["GraphicsConnection"]:
        """Returns a list of the GraphicsConnections item connected to this port."""
        return self.__connections

    def pos(self) -> QPointF:
        """Returns the position of the GraphicsPort (In terms of scene coordinates)."""
        return self.graphics_node.pos() + super().pos()

    def add_connection(self, connection_item):
        """Adds a new GraphicsConnection item to the list of connections.

        Args:
            connection_item: A GraphicsConnection object.
        """
        self.__connections.add(connection_item)

    def remove_connection(self, connection_item):
        """Removes an existent GraphicsConnection item from the list of connections.

        Doesn't do anything if the item to remove is not present on the connections
        list.

        Args:
            connection_item: A GraphicsConnection object.
        """
        self.__connections.discard(connection_item)

    def itemChange(self, change: QGraphicsItem.GraphicsItemChange, value):
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            # Update the position of all connections to follow the ports
            for connection in self.connections:
                connection.updatePath()

        return super().itemChange(change, value)

    def boundingRect(self) -> QRectF:
        """Returns the bounding rect of the port.

        Returns:
            A rect enclosing the port object.
        """
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
