# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Flag, auto
from typing import List

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import (
    QBrush,
    QColor,
    QFont,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsSceneHoverEvent,
    QGraphicsTextItem,
    QStyleOptionGraphicsItem,
    QWidget,
)

from dial.node_editor import Node

from .graphics_port import GraphicsPort


class GraphicsNode(QGraphicsItem):
    class State(Flag):
        NoFlags = 0
        ResizeLeft = auto()
        ResizeRight = auto()
        ResizeUp = auto()
        ResizeDown = auto()

    def __init__(self, node: Node, parent: QGraphicsItem = None):
        super().__init__(parent)

        # Components
        self.__node = node
        self.__node.graphics_node = self  # Add an instance variable to self

        self.__state = self.State.NoFlags

        # Graphic items
        self.__node_widget_proxy = QGraphicsProxyWidget(parent=self)

        self.__graphics_title = QGraphicsTextItem(parent=self)
        self.__input_graphics_ports: List["GraphicsPort"] = []
        self.__output_graphics_ports: List["GraphicsPort"] = []

        # Graphic parameters
        self.__title_font = QFont("Ubuntu", 10)

        self.round_edge_size = 10
        self.padding = 12
        self.resize_cursor_margin = 15

        # Colors/Pens/Brushes
        self.title_color = Qt.white
        self.title_background_brush = QBrush(QColor("#FF313131"))
        self.background_brush = QBrush(QColor("#E3212121"))

        self.outline_selected_color = QColor("#FFA637")
        self.outline_default_color = QColor("#000000")

        self.__outline_pen = QPen(self.outline_default_color)

        # Connections
        self.node.title_changed.connect(self.__update_title)

        self.__setup_ui()
        self.__create_graphic_ports()

    @property
    def proxy_widget(self):
        return self.__node_widget_proxy

    @property
    def node(self) -> Node:
        """Returns the associated node."""
        return self.__node

    def setInnerWidget(self, widget: QWidget):
        """Sets a new widget inside the node."""
        self.prepareGeometryChange()
        self.proxy_widget.setWidget(widget)
        self.recalculateGeometry()

    def __title_height(self):
        """Returns the height of the title graphics item."""
        return self.__graphics_title.boundingRect().height()

    def __setup_ui(self):
        """Configures the graphics item flags and widgets."""
        # GraphicsItem
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setAcceptHoverEvents(True)

        # Title
        self.__graphics_title.setDefaultTextColor(self.title_color)
        self.__graphics_title.setPlainText(self.node.title)

        self.__graphics_title.setPos(self.padding, 0)

        # Proxy widget
        self.__node_widget_proxy.setWidget(
            self.node.inner_widget if self.node.inner_widget else QWidget()
        )
        self.__node_widget_proxy.setPos(
            self.padding, self.__title_height() + self.padding
        )

    def __create_graphic_ports(self):
        """Adds new GraphicsPort items at each side of the node."""

        def create_ports(ports_dict, port_name_position, x_offset):
            graphics_ports = []
            for i, port in enumerate(ports_dict.values()):
                graphics_port = GraphicsPort(port, port_name_position, parent=self)
                graphics_port.setPos(
                    x_offset,
                    self.__title_height()
                    + graphics_port.radius * 4
                    + i * graphics_port.radius * 4,
                )
                graphics_ports.append(graphics_port)

            return graphics_ports

        self.__input_graphics_ports = create_ports(
            self.node.inputs, GraphicsPort.PortNamePosition.Left, x_offset=0
        )
        self.__output_graphics_ports = create_ports(
            self.node.outputs,
            GraphicsPort.PortNamePosition.Right,
            x_offset=self.boundingRect().width(),
        )

    def __update_title(self, new_text: str):
        """Updates the graphics title item with new text."""
        self.__graphics_title.setPlainText(new_text)

    def boundingRect(self) -> QRectF:
        """Returns the rect enclosing the node."""
        proxy_rect = self.__node_widget_proxy.boundingRect()

        return proxy_rect.adjusted(
            0, 0, self.padding * 2, self.__title_height() + self.padding * 2
        ).normalized()

    def itemChange(self, change, value):
        if change == self.ItemSelectedChange:
            self.__outline_pen.setColor(
                self.outline_selected_color if value else self.outline_default_color
            )
            if value:
                self.setZValue(10)
            else:
                self.setZValue(0)

            return value

        return super().itemChange(change, value)

    def hoverMoveEvent(self, event: QGraphicsSceneHoverEvent):
        x_pos = event.pos().x()
        y_pos = event.pos().y()

        # Horizontal margins
        if x_pos < self.resize_cursor_margin:
            self.__state |= self.State.ResizeLeft
            self.setCursor(Qt.SizeHorCursor)
        elif self.boundingRect().width() - x_pos < self.resize_cursor_margin:
            self.__state |= self.State.ResizeRight
            self.setCursor(Qt.SizeHorCursor)
        else:
            self.__state &= ~self.State.ResizeLeft
            self.__state &= ~self.State.ResizeRight

        if y_pos < self.resize_cursor_margin:
            self.__state |= self.State.ResizeUp
            self.setCursor(Qt.SizeVerCursor)
        elif self.boundingRect().height() - y_pos < self.resize_cursor_margin:
            self.__state |= self.State.ResizeDown
            self.setCursor(Qt.SizeVerCursor)
        else:
            self.__state &= ~self.State.ResizeUp
            self.__state &= ~self.State.ResizeDown

        if self.__state == (self.State.ResizeLeft | self.State.ResizeUp):
            self.setCursor(Qt.SizeFDiagCursor)

        if self.__state == (self.State.ResizeLeft | self.State.ResizeDown):
            self.setCursor(Qt.SizeBDiagCursor)

        if self.__state == (self.State.ResizeRight | self.State.ResizeUp):
            self.setCursor(Qt.SizeBDiagCursor)

        if self.__state == (self.State.ResizeRight | self.State.ResizeDown):
            self.setCursor(Qt.SizeFDiagCursor)

        if self.__state == self.State.NoFlags:
            self.unsetCursor()

        super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent):
        self.unsetCursor()
        self.__state = self.State.NoFlags

        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        self.start_resizing_x = event.pos().x()
        self.start_resizing_y = event.pos().y()

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.cursor() != Qt.ArrowCursor:
            self.prepareGeometryChange()

            diff_x = self.start_resizing_x - event.pos().x()
            diff_y = self.start_resizing_y - event.pos().y()

            self.start_resizing_x = event.pos().x()
            self.start_resizing_y = event.pos().y()

            new_x = 0
            new_y = 0
            new_w = 0
            new_h = 0

            if self.__state & self.State.ResizeLeft:
                new_x = -diff_x

            if self.__state & self.State.ResizeRight:
                new_w = -diff_x

            if self.__state & self.State.ResizeUp:
                new_y = -diff_y

            if self.__state & self.State.ResizeDown:
                new_h = -diff_y

                self.recalculateGeometry(new_x, new_y, new_w, new_h)

            return

        super().mouseMoveEvent(event)

    def recalculateGeometry(
        self, new_x: int = 0, new_y: int = 0, new_w: int = 0, new_h: int = 0
    ):
        self.__node_widget_proxy.setGeometry(
            self.__node_widget_proxy.geometry().adjusted(new_x, new_y, new_w, new_h)
        )

        self.setPos(self.pos().x() + new_x, self.pos().y() + new_y)

        self.__node_widget_proxy.setPos(
            self.padding, self.__title_height() + self.padding
        )

        for graphics_port in self.__output_graphics_ports:
            graphics_port.setX(self.boundingRect().width())

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        """Paints the GraphicsNode item."""

        self.__paint_background(painter)
        self.__paint_title_background(painter)
        self.__paint_outline(painter)

    def __paint_background(self, painter: QPainter):
        path_background = QPainterPath()
        path_background.addRoundedRect(
            self.boundingRect(), self.round_edge_size, self.round_edge_size
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.background_brush)

        painter.drawPath(path_background.simplified())

    def __paint_title_background(self, painter: QPainter):
        title_rect = self.__graphics_title.boundingRect()

        path_title_background = QPainterPath()
        path_title_background.setFillRule(Qt.WindingFill)
        path_title_background.addRoundedRect(
            0,
            0,
            self.boundingRect().width(),
            title_rect.height(),
            self.round_edge_size,
            self.round_edge_size,
        )

        # (Drawing rects to hide the two botton round edges)
        path_title_background.addRect(
            0,
            title_rect.height() - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        path_title_background.addRect(
            self.boundingRect().width() - self.round_edge_size,
            title_rect.height() - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.title_background_brush)
        painter.drawPath(path_title_background.simplified())

    def __paint_outline(self, painter: QPainter):
        path_outline = QPainterPath()
        path_outline.addRoundedRect(
            self.boundingRect(), self.round_edge_size, self.round_edge_size
        )

        painter.setPen(self.__outline_pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())
