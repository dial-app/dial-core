# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QBrush, QColor, QPainter, QPainterPath
from PySide2.QtWidgets import (
    QGraphicsItem,
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
        self.inner_widget = QPushButton("Testing")
        self.graphics_title = QGraphicsTextItem(self)

        # Colors/Pens/Brushes
        self.title_color = Qt.white
        self.background_brush = QBrush(QColor("#E3212121"))

        # Connections
        self.node.title_changed.connect(self.__update_title)

    @property
    def node(self) -> Node:
        """Returns the associated node."""
        return self.__node

    def __setup_ui(self):
        """Configures the graphics item flags and widgets."""
        # GraphicsItem
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemIsMovable)

        # Title
        self.graphics_title.setDefaultTextColor(self.title_color)
        self.graphics_title.setPlainText(self.node.title)

        self.graphics_title.setPos(0, 0)

    def __update_title(self, new_text: str):
        """Updates the graphics title item with new text."""
        self.graphics_title.setPlainText(new_text)

    def boundingRect(self) -> QRectF:
        """Returns the rect enclosing the node."""
        return QRectF(0, 0, 200, 200).normalized()

    def paint(
        self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: QWidget
    ):
        """Paints the GraphicsNode item."""
        path_background = QPainterPath()
        path_background.addRoundedRect(self.boundingRect(), 10, 10)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self.background_brush)

        painter.drawPath(path_background.simplified())
