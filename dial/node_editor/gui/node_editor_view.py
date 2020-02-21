# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Any, Union

from PySide2.QtCore import Qt
from PySide2.QtGui import QMouseEvent, QPainter, QWheelEvent
from PySide2.QtWidgets import QDialog, QGraphicsView, QPushButton, QVBoxLayout

from dial.misc.event_filters import PanningEventFilter
from dial.node_editor.gui import GraphicsConnection, GraphicsNode, GraphicsPort
from dial.utils import log


class NodeEditorView(QGraphicsView):
    def __init__(self, tabs_widget, parent=None):
        super().__init__(parent)

        self.scale_factor_increment = 0.2

        self.new_connection = None

        self.__tabs_widget = tabs_widget

        self.__mouse_button_press_event = {
            Qt.LeftButton: self.__start_dragging_connection,
        }

        self.__mouse_button_release_event = {
            Qt.LeftButton: self.__stop_dragging_connection,
        }

        self.__mouse_double_click_event = {Qt.LeftButton: self.__toggle_widget_dialog}

        self.__panning_event_filter = PanningEventFilter(parent=self)
        self.installEventFilter(self.__panning_event_filter)

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

    # def mousePressEvent(self, event: QMouseEvent):
    #     """Performs an action when any mouse button is pressed."""
    #     try:
    #         self.__mouse_button_press_event[event.button()](event)
    #     except KeyError:
    #         pass

    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     """Performs an action when any mouse button is pressed twice."""

    #     try:
    #         self.__mouse_double_click_event[event.button()](event)
    #     except KeyError:
    #         pass

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Performs an action when any mouse button is released."""
        # try:
        #     self.__mouse_button_release_event[event.button()](event)
        # except KeyError:
        #     pass
        event.ignore()
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        event.ignore()
        super().mouseReleaseEvent(event)

    # def mouseMoveEvent(self, event: QMouseEvent):
    #     """Performs an action when the mouse moves (while clicking a mouse button)."""
    #     if self.dragMode() == QGraphicsView.ScrollHandDrag:
    #         self.__panning_view(event)
    #     elif self.__is_dragging_connection():
    #         self.__dragging_connection(event)
    #     else:
    #         super().mouseMoveEvent(event)

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

    def __toggle_widget_dialog(self, event: QMouseEvent):
        """Shows the Node `inner_widget` on a new dialog. The content of the node is
        substituted with a button that hides the dialog and shows the inner_widget back
        in the node when pressed.
        """

        item = self.__item_clicked_on(event)

        if not isinstance(item, GraphicsNode):
            return

        # Don't create a dialog if the node doesn't has an inner_widget
        if not item.node.inner_widget:
            return

        node_inner_widget = item.node.inner_widget
        previous_node_size = node_inner_widget.size()

        show_here_button = QPushButton("Show here")
        show_here_button.setMinimumSize(200, 100)

        # Replace the node widget with the button
        item.setInnerWidget(show_here_button)

        # Create a new dialog for displaying the node widget
        dialog = QDialog(self)
        dialog.setWindowTitle(item.node.title)

        layout = QVBoxLayout()
        layout.addWidget(node_inner_widget)
        dialog.setLayout(layout)

        dialog.show()

        def place_widget_back_in_node():
            # Widgets embedded in nodes can't have parents
            node_inner_widget.setParent(None)

            node_inner_widget.resize(previous_node_size)
            item.setInnerWidget(node_inner_widget)

            dialog.close()

        # The widget will be displayed back in the node when the dialog is closed or
        # when the "show here" button is pressed
        dialog.finished.connect(place_widget_back_in_node)
        show_here_button.clicked.connect(place_widget_back_in_node)

    def __start_dragging_connection(self, event: QMouseEvent):
        """Starts creating a new connection by dragging the mouse.

        Only works when the user clicks on a GraphicsPort item.

        Args:
            event: Mouse event.
        """
        item = self.__item_clicked_on(event)

        if not isinstance(item, GraphicsPort):
            super().mousePressEvent(event)
            return

        log.get_logger(__name__).debug("Start dragging")

        self.new_connection = self.__create_new_connection()
        self.new_connection.start_graphics_port = item
        self.new_connection.end = self.new_connection.start_graphics_port.pos()

        GraphicsPort.drawing_state = GraphicsPort.DrawingState.Dragging
        GraphicsPort.drawing_type = item.port.port_type
        self.scene().update()

        # Its important to don't pass the event to parent classes to avoid selecting
        # items when we start dragging.
        # DON'T include `super().mousePressEvent(event)` here

    def __stop_dragging_connection(self, event: QMouseEvent):
        """Stops dragging the connection.

        If the connection doesn't end on a GraphicsPort, the connection item is removed
        from the scene.

        Args:
            event: Mouse event.
        """
        super().mouseReleaseEvent(event)

        if not self.__is_dragging_connection():
            return

        item = self.__item_clicked_on(event)

        # The conection must end on a COMPATIBLE GraphicsPort item
        if isinstance(item, GraphicsPort) and item.port.is_compatible_with(
            self.new_connection.start_graphics_port.port
        ):
            self.new_connection.end_graphics_port = item
        else:
            self.__remove_connection(self.new_connection)

        GraphicsPort.drawing_state = GraphicsPort.DrawingState.Normal
        GraphicsPort.drawing_type = None
        self.scene().update()

        # Reset the connection item
        self.new_connection = None

    def __dragging_connection(self, event: QMouseEvent):
        """Drags a connection while the mouse is moving.

        Args:
            event: Mouse event.
        """
        self.new_connection.end = self.mapToScene(event.pos())

        item = self.__item_clicked_on(event)
        if self.__clicked_on_graphics_port(item):
            self.new_connection.end = item.pos()

        super().mouseMoveEvent(event)

    def __is_dragging_connection(self) -> bool:
        """Checks if the user is currently dragging a connection or not."""
        return self.new_connection is not None

    def __create_new_connection(self) -> "GraphicsConnection":
        """Create a new connection on the scene."""
        connection = GraphicsConnection()
        self.scene().addItem(connection)

        return connection

    def __remove_connection(self, connection: "GraphicsConnection"):
        """Removes the GraphicsConnection item from the scene."""
        self.scene().removeItem(connection)

    def __item_clicked_on(self, event: QMouseEvent) -> Union["GraphicsPort", Any]:
        """Returns the graphical item under the mouse."""
        return self.itemAt(event.pos())
