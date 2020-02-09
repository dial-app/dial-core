# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from PySide2.QtCore import QEvent, Qt
from PySide2.QtGui import QMouseEvent, QPainter
from PySide2.QtWidgets import QGraphicsView


class NodeEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__()

    def __setup_ui(self):
        self.setRenderHints(
            QPainter.Antialiasing
            | QPainter.HighQualityAntialiasing
            | QPainter.TextAntialiasing
            | QPainter.SmoothPixmapTransform
        )

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.zoomInFactor = 1.25
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

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

    def wheelFactor(self, event):
        zoomOutFactor = 1 / self.zoomInFactor
