# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent, QPainter
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

    def mousePressEvent(self, event: QMouseEvent):
        """Performs an action when any mouse button is pressed."""
        if event.button() == Qt.MiddleButton:
            self.__start_panning_view(event)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Performs an action when any mouse button is released."""
        if event.button() == Qt.MiddleButton:
            self.__stop_panning_view()

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        """Performs an action when the mouse moves (while clicking a mouse button)."""

        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.__panning_view(event)

        super().mouseMoveEvent(event)

    def __start_panning_view(self, event: QMouseEvent):
        """Responds to the event of start dragging the view for panning it."""
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.panning_start_x = event.x()
        self.panning_start_y = event.y()

    def __panning_view(self, event: QMouseEvent):
        """Pans the view using the mouse movement."""

        # Move view by using the scrollbars
        self.horizontalScrollBar().setValue(
            self.horizontalScrollBar().value() - (event.x() - self.panning_start_x)
        )

        self.verticalScrollBar().setValue(
            self.verticalScrollBar().value() - (event.y() - self.panning_start_y)
        )

        # Set new "last panning values"
        self.panning_start_x = event.x()
        self.panning_start_y = event.y()

    def __stop_panning_view(self):
        """Responds to the event of start dragging the view for panning it."""
        self.setDragMode(QGraphicsView.NoDrag)
