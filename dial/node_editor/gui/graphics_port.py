# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING, Set

from PySide2.QtCore import QPointF, QRectF, Qt
from PySide2.QtGui import (
    QBrush,
    QColor,
    QPainter,
    QPainterPath,
    QPainterPathStroker,
    QPen,
)
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

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

    class DrawingState(Enum):
        Normal = 0
        Dragging = 1

    class PortNamePosition(Enum):
        Left = 0
        Right = 1

    drawing_state = DrawingState.Normal
    drawing_type = None

    def __init__(
        self, port: Port, port_name_position: PortNamePosition, parent: "GraphicsNode",
    ):
        super().__init__(parent)

        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges)

        self.graphics_node = parent

        self.setCursor(Qt.ArrowCursor)

        self.__port = port

        # Add add an instance attribute to this GraphicsPort.
        self.__port.graphics_port = self  # type: ignore

        self.__connections: Set["GraphicsConnection"] = set()

        self.radius = 8
        self.margin = 12

        self.__port_name_position = port_name_position
        self.__port_name = QGraphicsTextItem(parent=self)
        self.__port_name.setPlainText(self.__port.name)
        self.__port_name.setDefaultTextColor("#FFFFFF")
        self.__port_name.setFlag(QGraphicsItem.ItemStacksBehindParent)

        if self.__port_name_position == self.PortNamePosition.Left:
            self.__port_name.setPos(-self.__port_name.boundingRect().width() - 3, 1)
        elif self.__port_name_position == self.PortNamePosition.Right:
            self.__port_name.setPos(3, 1)

        # Colors/Pens/Brushes
        self.__color = TypeColor.get_color_for(port.port_type)

        self.outline_pen = QPen(self.__color.darker())
        self.outline_pen.setWidthF(2)
        self.background_brush = QBrush(self.__color)

        self.dashed_outline_pen = QPen(self.__color)
        self.dashed_outline_pen.setStyle(Qt.DashLine)
        self.dashed_outline_pen.setWidth(2)

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
        """Returns an enclosing rect for the port, PLUS a margin. All the boundingRect()
        area is clickable by the user and can be used as a start/end zone for drag/drop
        connections.

        Important:
            Do not use this function for painting. The area for painting doesn't
            includes the margins, only the radius.
        """
        return QRectF(
            -self.radius - self.margin,
            -self.radius - self.margin,
            2 * self.radius + 2 * self.margin,
            2 * self.radius + 2 * self.margin,
        )

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionGraphicsItem,
        widget: QWidget = None,
    ):
        """Paints the port."""
        painter.setPen(self.outline_pen)
        painter.setBrush(self.background_brush)
        painter.drawEllipse(
            -self.radius, -self.radius, 2 * self.radius, 2 * self.radius
        )

        if (
            GraphicsPort.drawing_state == GraphicsPort.DrawingState.Dragging
            and self.port.port_type == GraphicsPort.drawing_type
        ):
            painter.setPen(self.dashed_outline_pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(self.boundingRect())
