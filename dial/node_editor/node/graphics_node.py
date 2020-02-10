# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QBrush, QColor, QFont, QPainter, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QGraphicsProxyWidget, QGraphicsTextItem

from dial.node_editor.socket import Socket


class GraphicsNode(QGraphicsItem):
    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.node = node

        # Components
        self.graphics_content = QGraphicsProxyWidget(self)

        # Appearance
        self.__title_color = Qt.white
        self.__title_font = QFont("Ubuntu", 10)

        self.round_edge_size = 10

        self.title_height = 24
        self.padding = 13.0

        self.title_background_brush = QBrush(QColor("#FF313131"))
        self.background_brush = QBrush(QColor("#E3212121"))
        self.outline_default_pen = QPen(QColor("#7F000000"))
        self.outline_selection_pen = QPen(QColor("#FFFFA637"))

        self.__setup_ui()

    def __setup_ui(self):
        # GraphicsItem
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # Content
        self.graphics_content.setWidget(self.node.content)
        self.graphics_content.setPos(self.padding, self.padding + self.title_height)

        # Title
        self.title_item = QGraphicsTextItem(self,)
        self.title_item.setDefaultTextColor(self.__title_color)
        self.title_item.setFont(self.__title_font)
        self.title_item.setPlainText(self.node.title)

        self.title_item.setPos(self.padding, 0)
        self.title_item.setTextWidth(self.boundingRect().width())

        # Sockets
        def position_sockets(sockets):
            for socket in sockets:
                socket.graphics_socket.setParentItem(self)
                if socket.position == Socket.Position.LeftTop:
                    x = 0
                else:
                    x = self.boundingRect().width()

                socket.graphics_socket.setPos(
                    x,
                    self.title_height * 1.5
                    + socket.index * socket.graphics_socket.boundingRect().height() * 2,
                )

        position_sockets(self.node.inputs)
        position_sockets(self.node.outputs)

    @property
    def title(self):
        """Returns the title of the node"""
        return self.node.title

    @title.setter
    def title(self, value):
        """Sets a new title for the node"""
        self.node.title = value
        self.title_item.setPlainText(self.node.title)

    def boundingRect(self):
        rect = self.graphics_content.rect()
        return QRectF(
            0,
            0,
            rect.width() + self.padding * 2,
            rect.height() + self.title_height + self.padding * 2,
        ).normalized()

    def paint(self, painter: QPainter, option, widget=None):
        # Draw title background
        path_title_background = QPainterPath()
        path_title_background.setFillRule(Qt.WindingFill)
        path_title_background.addRoundedRect(
            0,
            0,
            self.boundingRect().width(),
            self.title_height,
            self.round_edge_size,
            self.round_edge_size,
        )
        # (Drawing to rects to hide the two botton round edges)
        path_title_background.addRect(
            0,
            self.title_height - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        path_title_background.addRect(
            self.boundingRect().height() - self.round_edge_size,
            self.title_height - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.title_background_brush)
        painter.drawPath(path_title_background.simplified())

        # Draw node background
        path_background = QPainterPath()
        path_background.addRoundedRect(
            self.boundingRect(), self.round_edge_size, self.round_edge_size
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.background_brush)
        painter.drawPath(path_background.simplified())

        # Draw node outline
        painter.setPen(
            self.outline_default_pen
            if not self.isSelected()
            else self.outline_selection_pen
        )
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_background.simplified())
