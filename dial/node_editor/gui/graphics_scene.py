# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import math
from typing import TYPE_CHECKING, List, Tuple

from PySide2.QtCore import QLine, QRect
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QGraphicsScene

from dial.utils.log import DEBUG, log_on_end

from .graphics_node import GraphicsNode

if TYPE_CHECKING:
    from PySide2.QtWidgets import QObject
    from PySide2.QtCore import QRectF
    from dial.node_editor import Node, Scene
    from PySide2.QtGui import QPainter


class GraphicsScene(QGraphicsScene):
    def __init__(self, scene: "Scene", parent: "QObject" = None):
        super().__init__(parent)

        self.__scene = scene

        # Settings
        self.width = 64000
        self.height = 64000

        self.grid_size = 20
        self.grid_squares = 5

        # Colors/Pens/Brushes
        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)

        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)

        # Connections
        self.scene.node_added.connect(self.add_node_to_graphics)

        # UI
        self.__setup_ui()

    @property
    def scene(self):
        """Returns the scene attached to this graphics scene."""
        return self.__scene

    def __setup_ui(self):
        """Configure the graphics scene object."""
        self.setBackgroundBrush(self._color_background)

        self.setSceneRect(
            -self.width // 2, -self.height // 2, self.width, self.height,
        )

    @log_on_end(DEBUG, "{node} added as a GraphicNode.")
    def add_node_to_graphics(self, node: "Node"):
        """Add a new Node to the GraphicsScene, making it visible."""
        self.addItem(GraphicsNode(node))

    def drawBackground(self, painter: "QPainter", rect: "QRectF"):
        """Draws the background for the scene."""
        super().drawBackground(painter, rect)

        grid_rect = self.__calculate_grid_boundaries(rect)

        # Compute all lines to be drawn
        light_lines, dark_lines = self.__calculate_grid_lines(grid_rect)

        # Draw all lines
        painter.setPen(self._pen_light)
        painter.drawLines(light_lines)

        painter.setPen(self._pen_dark)
        painter.drawLines(dark_lines)

    def __calculate_grid_boundaries(self, rect: "QRectF") -> "QRect":
        """Calculates the grid boundaries from the rect."""
        # Get grid boundaries
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        # Anchor left and top to the closest grid line
        left = left - (left % self.grid_size)
        top = top - (top % self.grid_size)

        return QRect(left, top, right - left + 2, bottom - top + 2)

    def __calculate_grid_lines(self, grid_rect: "QRect") -> Tuple[List, List]:
        """Calculates the coordinates of the horizontal/vertical lines to be drawn.

        Args:
            grid_rect: Rectangle representing the grid boundaries.

        Returns:
            Lists of light lines and dark lines to draw.
        """
        light_lines = []
        dark_lines = []

        # Calculate horizontal lines
        for x in range(grid_rect.left(), grid_rect.right(), self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                light_lines.append(QLine(x, grid_rect.top(), x, grid_rect.bottom()))
            else:
                dark_lines.append(QLine(x, grid_rect.top(), x, grid_rect.bottom()))

        # Calculate vertical lines
        for y in range(grid_rect.top(), grid_rect.bottom(), self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                light_lines.append(QLine(grid_rect.left(), y, grid_rect.right(), y))
            else:
                dark_lines.append(QLine(grid_rect.left(), y, grid_rect.right(), y))

        return light_lines, dark_lines
