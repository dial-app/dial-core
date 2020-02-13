# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt
from PySide2.QtGui import QPainter
from PySide2.QtWidgets import QGraphicsView


class NodeEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.__setup_ui()

    def __setup_ui(self):
        """Setups the UI configuration."""
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.HighQualityAntialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        # Hide scrollbars
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Set anchor under mouse (for zooming)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
