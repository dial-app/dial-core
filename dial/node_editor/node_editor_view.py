# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from enum import Enum

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent, QPainter
from PySide2.QtWidgets import QGraphicsView

from dial.node_editor.edge import Edge
from dial.node_editor.socket import GraphicsSocket


class NodeEditorView(QGraphicsView):
    class Mode(Enum):
        Idle = 1
        EdgeDrag = 2

    def __init__(self, parent=None):
        super().__init__()

        self.mode = self.Mode.Idle

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
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)

    def leftMouseButtonPress(self, event):
        item = self.__get_item_at_click(event)

        self.last_lmb_click_scene_pos = self.mapToScene(event.pos())

        if type(item) is GraphicsSocket:
            if self.mode == self.Mode.Idle:
                self.edge_drag_start(item)
                return

        if self.mode == self.Mode.EdgeDrag:
            self.edge_drag_end(item)

        super().mousePressEvent(event)

    def leftMouseButtonRelease(self, event):
        item = self.__get_item_at_click(event)

        if self.mode == self.Mode.EdgeDrag:
            new_lmb_release_scene_pos = self.mapToScene(event.pos())

            dist_scene = new_lmb_release_scene_pos - self.last_lmb_click_scene_pos

            if dist_scene.x() * dist_scene.x() + dist_scene.y() * dist_scene.y() > 20:
                self.edge_drag_end(item)

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.mode == self.Mode.EdgeDrag:
            pos = self.mapToScene(event.pos())
            self.dragEdge.graphics_edge.set_destination(pos.x(), pos.y())
            self.dragEdge.graphics_edge.update()

        super().mouseMoveEvent(event)

    def edge_drag_start(self, item):
        self.mode = self.Mode.EdgeDrag
        self.mode = self.Mode.EdgeDrag

        self.dragEdge = Edge(item.socket, None)
        self.scene().scene.addEdge(self.dragEdge)

        print("Start dragging edge")
        print("Assign Start Socket")

    def edge_drag_end(self, item):
        self.mode = self.Mode.Idle
        print("End dragging")

        if type(item) is GraphicsSocket:
            print("Assign End Socket")
            return True

        return False

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

    def rightMouseButtonPress(self, event):
        super().mouseReleaseEvent(event)

    def rightMouseButtonRelease(self, event):
        super().mousePressEvent(event)

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

    def __get_item_at_click(self, event):
        return self.itemAt(event.pos())
