# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum, Flag, auto
from typing import TYPE_CHECKING

from PySide2.QtCore import QEvent, QObject, Qt

if TYPE_CHECKING:
    from dial.gui.node_editor import GraphicsNode


class ResizableItemEventFilter(QObject):
    """The ResizableItemEventFilter class provides resizing anchors for a GraphicsNode
    object.

    The anchors can be dragged freely using the mouse, and the node will be resized
    accordingly.

    Important:
        This filter only works with a GraphicsNode object.

    Attributes:
        resize_margins: Size of the margins that can be clicked to start the resizing
        event.
        button_used_for_resizing: The button that mast be pressed and dragged for
        resizing the node.

    Examples:
        node = GraphicsNode()
        resizable_item_event_filter = ResizableItemEventFilter()

        node.installEventFilter(resizable_item_event_filter)
    """

    class State(Enum):
        Idle = 0
        Resizing = 1

    class MarginClicked(Flag):
        NoMargin = 0
        Top = auto()
        Bottom = auto()
        Left = auto()
        Right = auto()

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__state = self.State.Idle
        self.__margins_clicked = self.MarginClicked.NoMargin

        self.resize_margins = 12

        self.button_used_for_resizing = Qt.LeftButton

    @property
    def state(self) -> "ResizableItemEventFilter.State":
        """Returns the state of the event filter (Normal, Resizing...)"""
        return self.__state

    def is_resizing(self) -> bool:
        """Checks if the event filter is currently resizing an object."""
        return self.__state == self.State.Resizing

    def eventFilter(self, item: "QObject", event: "QEvent") -> bool:
        """Tracks the mouse movements to do the actual resizing.

        When the mouse hovers over the node, the cursor icon is changed to reflect the
        direction of the resizing (P.E: If the mouse is on the left side of the node, a
        <-> icon will appear).

        When the resizing button is clicked, the node will be resized until the button
        is released.
        """
        if event.type() == QEvent.GraphicsSceneHoverMove:
            self.__track_margins_under_cursor(item, event)
            return True

        if self.__resize_button_clicked(event) and self.__is_inside_resize_margins(
            item, event
        ):
            self.__start_resizing_node(item, event)
            return True

        if self.is_resizing():
            if event.type() == QEvent.GraphicsSceneMouseMove:
                self.__resizing_node(item, event)
                return True

            if self.__resize_button_released(event):
                self.__stop_resizing_node(item, event)
                return True

        return super().eventFilter(item, event)

    def __resize_button_clicked(self, event: "QEvent") -> bool:
        """Checks if the button designed for resizing was pressed."""
        return (
            event.type() == QEvent.GraphicsSceneMousePress
            and event.button() == self.button_used_for_resizing
        )

    def __resize_button_released(self, event: "QEvent") -> bool:
        """Checks if the button designed for resizing was released."""
        return (
            event.type() == QEvent.GraphicsSceneMouseRelease
            and event.button() == self.button_used_for_resizing
        )

    def __start_resizing_node(self, node: "GraphicsNode", event: "QEvent"):
        """Starts resizing the node.

        Saves some positions for reference during the resizing event.
        """
        self.__state = self.State.Resizing

        # Saves some information of the cursor and the node prior to resizing
        self.__initial_resize_pos = event.scenePos()
        self.__initial_node_pos = node.pos()
        self.__initial_node_size = node.proxy_widget.size()

    def __resizing_node(self, node: "GraphicsNode", event: "QEvent"):
        """Resizes the node while dragging one of the margins. Calculates the resulting
        size and position of the node and applies it."""
        diff = event.scenePos() - self.__initial_resize_pos

        new_x = 0
        new_y = 0
        new_w = 0
        new_h = 0

        if self.__margins_clicked & self.MarginClicked.Left:
            new_x = (
                diff.x()
                if node.proxy_widget.size().width()
                > node.proxy_widget.minimumSize().width()
                else self.__initial_node_size.width()
                - node.proxy_widget.minimumSize().width()
            )
            new_w = -diff.x()

        elif self.__margins_clicked & self.MarginClicked.Right:
            new_w = diff.x()

        if self.__margins_clicked & self.MarginClicked.Top:
            new_y = (
                diff.y()
                if node.proxy_widget.size().height()
                > node.proxy_widget.minimumSize().height()
                else self.__initial_node_size.height()
                - node.proxy_widget.minimumSize().height()
            )
            new_h = -diff.y()

        elif self.__margins_clicked & self.MarginClicked.Bottom:
            new_h = diff.y()

        node.prepareGeometryChange()

        node.proxy_widget.resize(
            self.__initial_node_size.width() + new_w,
            self.__initial_node_size.height() + new_h,
        )
        node.setPos(
            self.__initial_node_pos.x() + new_x, self.__initial_node_pos.y() + new_y
        )

        node.recalculateGeometry()

    def __stop_resizing_node(self, node: "GraphicsNode", event: "QEvent"):
        """Stops resizing the node."""
        self.__state = self.State.Idle

    def __is_inside_resize_margins(self, node: "GraphicsNode", event: "QEvent") -> bool:
        """Checks if the cursor is currently on the margins of the node."""
        return self.__margins_clicked != self.MarginClicked.NoMargin

    def __track_margins_under_cursor(self, node: "GraphicsNode", event: "QEvent"):
        """Sets different flags marking on top of which margin the cursor is."""
        x_pos = event.pos().x()
        y_pos = event.pos().y()

        # Horizontal margins
        if x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Left
            node.setCursor(Qt.SizeHorCursor)
        elif node.boundingRect().width() - x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Right
            node.setCursor(Qt.SizeHorCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Left
            self.__margins_clicked &= ~self.MarginClicked.Right

        # Vertical margins
        if y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Top
            node.setCursor(Qt.SizeVerCursor)
        elif node.boundingRect().height() - y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Bottom
            node.setCursor(Qt.SizeVerCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Top
            self.__margins_clicked &= ~self.MarginClicked.Bottom

        if self.__margins_clicked == (self.MarginClicked.Left | self.MarginClicked.Top):
            node.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Left | self.MarginClicked.Bottom
        ):
            node.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Top
        ):
            node.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Bottom
        ):
            node.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == self.MarginClicked.NoMargin:
            node.unsetCursor()
