# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

from PySide2.QtCore import QPointF, Qt
from PySide2.QtGui import QMouseEvent, QPainter, QWheelEvent
from PySide2.QtWidgets import QGraphicsView

from dial.node_editor.gui import GraphicsConnection, GraphicsPort


class NodeEditorView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.scale_factor_increment = 0.2

        self.new_connection = None

        self.__mouse_button_press_event = {
            Qt.MiddleButton: self.__start_panning_view,
            Qt.LeftButton: self.__start_dragging_connection,
        }

        self.__mouse_button_release_event = {
            Qt.MiddleButton: self.__stop_panning_view,
            Qt.LeftButton: self.__stop_dragging_connection,
        }

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
        try:
            self.__mouse_button_press_event[event.button()](event)
        except KeyError:
            pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Performs an action when any mouse button is released."""
        try:
            self.__mouse_button_release_event[event.button()](event)
        except KeyError:
            pass

    def mouseMoveEvent(self, event: QMouseEvent):
        """Performs an action when the mouse moves (while clicking a mouse button)."""
        if self.dragMode() == QGraphicsView.ScrollHandDrag:
            self.__panning_view(event)

        if self.__is_dragging_connection():
            self.__dragging_connection(event)

        super().mouseMoveEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """Zooms in/out the view using the mouse wheel."""
        if event.delta() > 0:
            self.scale(
                1.0 + self.scale_factor_increment, 1.0 + self.scale_factor_increment
            )
        else:
            self.scale(
                1.0 - self.scale_factor_increment, 1.0 - self.scale_factor_increment
            )

        event.accept()

    def __start_panning_view(self, event: QMouseEvent):
        """Responds to the event of start dragging the view for panning it.

        Changes the mouse icon to a dragging hand, and saves the last clicked position
        used for calculate the mouse displacement.

        Args:
            event: Mouse event.
        """
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.panning_start_x = event.x()
        self.panning_start_y = event.y()

        super().mousePressEvent(event)

    def __stop_panning_view(self, event: QMouseEvent):
        """Responds to the event of start dragging the view for panning it.

        Changes the mouse icon back to the default icon.

        Args:
            event: Mouse event.
        """
        self.setDragMode(QGraphicsView.NoDrag)

        super().mouseReleaseEvent(event)

    def __panning_view(self, event: QMouseEvent):
        """Pans the view using the mouse movement.

        The scrollbars are moved along the view (They're disabled by default, but if
        enabled they could be usable).

        Args:
            event: Mouse event.
        """
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

        super().mouseMoveEvent(event)

    def __start_dragging_connection(self, event: QMouseEvent):
        """Starts creating a new connection by dragging the mouse.

        Only works when the user clicks on a GraphicsPort item.

        Args:
            event: Mouse event.
        """

        item = self.__item_clicked_on(event)

        if self.__clicked_on_graphics_port(item):
            self.new_connection = self.__create_new_connection()
            self.new_connection.start_graphics_port = item

            # Its important to not pass the event to parent classes to avoid selecting
            # items when we start dragging. That's why we return here.
            return

        super().mousePressEvent(event)

    def __stop_dragging_connection(self, event: QMouseEvent):
        """Stops dragging the connection.

        If the connection doesn't end on a GraphicsPort, the connection item is removed
        from the scene.

        Args:
            event: Mouse event.
        """
        if not self.__is_dragging_connection():
            return

        item = self.__item_clicked_on(event)

        # The conection must end on a GraphicsPort item
        if self.__clicked_on_graphics_port(item):
            self.new_connection.end_graphics_port = item
        else:
            self.__remove_connection(self.new_connection)

        # Reset the connection item
        self.new_connection = None

        super().mouseReleaseEvent(event)

    def __dragging_connection(self, event: QMouseEvent):
        """Drags a connection while the mouse is moving.

        Args:
            event: Mouse event.
        """
        self.new_connection.end = self.mapToScene(event.pos())

    def __is_dragging_connection(self) -> bool:
        """Checks if the user is currently dragging a connection or not."""
        return self.new_connection is not None

    def __create_new_connection(self) -> GraphicsConnection:
        """Create a new connection on the scene."""
        connection = GraphicsConnection()
        self.scene().addItem(connection)

        return connection

    def __remove_connection(self, connection: GraphicsConnection):
        """Removes the GraphicsConnection item from the scene."""
        self.scene().removeItem(connection)

    def __item_clicked_on(self, event: QMouseEvent):
        """Returns the graphical item under the mouse."""
        return self.itemAt(event.pos())

    def __clicked_on_graphics_port(self, item):
        """Checks if the passed item is a GraphicsPort or not."""
        return isinstance(item, GraphicsPort)
