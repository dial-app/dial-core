# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import math

from PySide2.QtCore import QLine
from PySide2.QtGui import QColor, QPen
from PySide2.QtWidgets import QGraphicsScene


class GraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None):
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
        self.scene.node_added.connect(self.__add_node_to_graphics)

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

    def drawBackground(self, painter, rect):
        """Draws the background for the scene."""
        super().drawBackground(painter, rect)

        # Get grid boundaries
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.grid_size)
        first_top = top - (top % self.grid_size)

        # Compute all lines to be drawn
        lines_light = []
        lines_dark = []

        # TODO: Remove duplication?
        for x in range(first_left, right, self.grid_size):
            if x % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.grid_size):
            if y % (self.grid_size * self.grid_squares) != 0:
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        # Draw all lines
        painter.setPen(self._pen_light)
        painter.drawLines(lines_light)

        painter.setPen(self._pen_dark)
        painter.drawLines(lines_dark)

    def __add_node_to_graphics(self, node):
        print("Add node to graphics")
