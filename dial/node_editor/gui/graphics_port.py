# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING, Set

from PySide2.QtCore import QPointF, QRectF
from PySide2.QtGui import QBrush, QColor, QPainter, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget

from dial.node_editor import Port

from .type_colors import TypeColor

if TYPE_CHECKING:
    from .graphics_connection import GraphicsConnection
    from .graphics_node import GraphicsNode

"""Class representing a port for a node.

Can be used as a start/end point for dragging connections between nodes.
"""


class GraphicsPort(QGraphicsItem):
    """Class representing a port for a node.

    Can be used as a start/end point for dragging connections between nodes.

    Attributes:
        graphics_node: Parent GraphicsNode object where this port is located.
        radius: Radius of the port (used for drawing).
        color: Color of the port.
        port: Port object associated with this GraphicsPort object.
        connections: GraphicsConnection objects connected to this port.
    """

    def __init__(self, port: Port, parent: "GraphicsNode"):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        self.graphics_node = parent

        self.__port = port

        # Add add an instance attribute to this GraphicsPort.
        self.__port.graphics_port = self  # type: ignore

        self.__connections: Set["GraphicsConnection"] = set()

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
    def port(self):
        """Returns the port associated to this GraphicsItem."""
        return self.__port

    @property
    def connections(self) -> Set["GraphicsConnection"]:
        """Returns a list of the GraphicsConnections item connected to this port."""
        return self.__connections

    def pos(self) -> QPointF:
        """Returns the position of the GraphicsPort (In terms of scene coordinates)."""
        return self.graphics_node.pos() + super().pos()

    def add_connection(self, connection_item: "GraphicsConnection"):
        """Adds a new GraphicsConnection item to the list of connections.

        Args:
            connection_item: A GraphicsConnection object.
        """
        self.__connections.add(connection_item)

    def remove_connection(self, connection_item: "GraphicsConnection"):
        """Removes an existent GraphicsConnection item from the list of connections.

        Doesn't do anything if the item to remove is not present on the connections
        list.

        Args:
            connection_item: A GraphicsConnection object.
        """
        self.__connections.discard(connection_item)

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
