# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent, QPainter
from PySide2.QtWidgets import QGraphicsView


class NodeEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()

        self.zoom_in_factor = 1.25
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        self.__setup_ui()

    def __setup_ui(self):
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

    def mousePressEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def middleMouseButtonPress(self, event):
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        # Emit a left mouse click (default button for drag mode)
        pressEvent = QMouseEvent(
            event.type(),
            event.localPos(),
            event.screenPos(),
            Qt.LeftButton,
            event.buttons() | Qt.LeftButton,
            event.modifiers(),
        )

        super().mousePressEvent(pressEvent)

    def middleMouseButtonRelease(self, event):
        self.setDragMode(QGraphicsView.NoDrag)

    def wheelEvent(self, event):
        zoom_out_factor = 1 / self.zoom_in_factor

        old_pos = self.mapToScene(event.pos())

        if event.angleDelta().y() > 0:
            zoom_factor = self.zoom_in_factor
            self.zoom += self.zoomStep
        else:
            zoom_factor = zoom_out_factor
            self.zoom -= self.zoomStep

        # Set new scale
        self.scale(zoom_factor, zoom_factor)

        # Translate view
        new_pos = self.mapToScene(event.pos())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())
