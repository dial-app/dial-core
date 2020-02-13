# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import (
    QBrush,
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPainterPath,
    QPen,
)
from PySide2.QtWidgets import (
    QGraphicsItem,
    QGraphicsProxyWidget,
    QGraphicsTextItem,
    QPushButton,
    QStyleOptionGraphicsItem,
    QWidget,
)

from dial.node_editor import Node


class GraphicsNode(QGraphicsItem):
    def __init__(self, node: Node, parent: QGraphicsItem = None):
        super().__init__(parent)

        # Components
        self.__node = node

        # Graphic items
        self.__node_widget_proxy = QGraphicsProxyWidget(parent=self)
        self.__graphics_title = QGraphicsTextItem(parent=self)

        # Graphic parameters
        self.__title_font = QFont("Ubuntu", 10)

        self.round_edge_size = 10
        self.padding = 15

        # Colors/Pens/Brushes
        self.title_color = Qt.white
        self.title_background_brush = QBrush(QColor("#FF313131"))
        self.background_brush = QBrush(QColor("#E3212121"))
        self.outline_default_pen = QPen(QColor("#7F000000"))
        self.outline_selection_pen = QPen(QColor("#FFFFA637"))

        # Connections
        self.node.title_changed.connect(self.__update_title)

        self.__setup_ui()

    @property
    def node(self) -> Node:
        """Returns the associated node."""
        return self.__node

    def __title_height(self):
        """Returns the height of the title graphics item."""
        return self.__graphics_title.boundingRect().height()

    def __setup_ui(self):
        """Configures the graphics item flags and widgets."""
        # GraphicsItem
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

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

    def __update_title(self, new_text: str):
        """Updates the graphics title item with new text."""
        self.__graphics_title.setPlainText(new_text)

    def boundingRect(self) -> QRectF:
        """Returns the rect enclosing the node."""
        proxy_rect = self.__node_widget_proxy.boundingRect()

        return proxy_rect.adjusted(
            0, 0, self.padding * 2, self.__title_height() + self.padding * 2
        )

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        """Paints the GraphicsNode item."""

        # Draw the background
        path_background = QPainterPath()
        path_background.addRoundedRect(
            self.boundingRect(), self.round_edge_size, self.round_edge_size
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.background_brush)

        painter.drawPath(path_background.simplified())

        # Draw the title background
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
            self.boundingRect().height() - self.round_edge_size,
            title_rect.height() - self.round_edge_size,
            self.round_edge_size,
            self.round_edge_size,
        )

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.title_background_brush)
        painter.drawPath(path_title_background.simplified())

        # Draw the outline
        painter.setPen(
            self.outline_default_pen
            if not self.isSelected()
            else self.outline_selection_pen
        )
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_background.simplified())
