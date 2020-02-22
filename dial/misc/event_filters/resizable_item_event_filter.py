# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# TODO: Make specific for GraphicsNode or truly generic

from enum import Enum, Flag, auto

from PySide2.QtCore import QEvent, QObject, QRectF, Qt
from PySide2.QtWidgets import QGraphicsItem, QGraphicsSceneMouseEvent


class ResizableItemEventFilter(QObject):
    class State(Enum):
        Idle = 0
        Resizing = 1

    class MarginClicked(Flag):
        NoMargin = 0
        Top = auto()
        Bottom = auto()
        Left = auto()
        Right = auto()

    def __init__(self, parent: QGraphicsItem = None):
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

    def eventFilter(self, item: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.GraphicsSceneHoverMove:
            self.__track_margins_under_cursor(item, event)
            return True

        if self.__resize_button_clicked(event) and self.__is_inside_resize_margins(
            item, event
        ):
            self.__start_resizing_item(item, event)
            return True

        if self.is_resizing():
            if event.type() == QEvent.GraphicsSceneMouseMove:
                self.__resizing_item(item, event)
                return True

            if self.__resize_button_released(event):
                self.__stop_resizing_item(item, event)
                return True

        return super().eventFilter(item, event)

    def __resize_button_clicked(self, event: QEvent) -> bool:
        """Checks if the button designed for resizing was pressed."""
        return (
            event.type() == QEvent.GraphicsSceneMousePress
            and event.button() == self.button_used_for_resizing
        )

    def __resize_button_released(self, event: QEvent) -> bool:
        """Checks if the button designed for resizing was released."""
        return (
            event.type() == QEvent.GraphicsSceneMouseRelease
            and event.button() == self.button_used_for_resizing
        )

    def __start_resizing_item(self, item: QGraphicsItem, event: QEvent):
        """Starts resizing the item."""
        self.__state = self.State.Resizing

        # Saves some information of the cursor and the item prior to resizing
        self.__initial_resize_pos = event.scenePos()
        self.__initial_item_pos = item.pos()
        self.__initial_item_size = item.proxy_widget.size()

    def __resizing_item(self, item: QGraphicsItem, event: QEvent):
        """Resize the item while dragging one of the margins. Calculates the resulting
        size and position of the node."""
        diff = event.scenePos() - self.__initial_resize_pos

        new_x = 0
        new_y = 0
        new_w = 0
        new_h = 0

        if self.__margins_clicked & self.MarginClicked.Left:
            new_x = (
                diff.x()
                if item.proxy_widget.size().width()
                > item.proxy_widget.minimumSize().width()
                else self.__initial_item_size.width()
                - item.proxy_widget.minimumSize().width()
            )
            new_w = -diff.x()

        elif self.__margins_clicked & self.MarginClicked.Right:
            new_w = diff.x()

        if self.__margins_clicked & self.MarginClicked.Top:
            new_y = (
                diff.y()
                if item.proxy_widget.size().height()
                > item.proxy_widget.minimumSize().height()
                else self.__initial_item_size.height()
                - item.proxy_widget.minimumSize().height()
            )
            new_h = -diff.y()

        elif self.__margins_clicked & self.MarginClicked.Bottom:
            new_h = diff.y()

        item.prepareGeometryChange()

        item.proxy_widget.resize(
            self.__initial_item_size.width() + new_w,
            self.__initial_item_size.height() + new_h,
        )
        item.setPos(
            self.__initial_item_pos.x() + new_x, self.__initial_item_pos.y() + new_y
        )

        item.recalculateGeometry()

    def __stop_resizing_item(self, item: QGraphicsItem, event: QEvent):
        """Stops resizing the item."""
        self.__state = self.State.Idle

    def __is_inside_resize_margins(self, item: QGraphicsItem, event: QEvent) -> bool:
        """Checks if the cursor is currently on the margins of the item."""
        return self.__margins_clicked != self.MarginClicked.NoMargin

    def __track_margins_under_cursor(self, item: QGraphicsItem, event: QEvent):
        """Sets different flags marking on top of which margin the cursor is."""
        x_pos = event.pos().x()
        y_pos = event.pos().y()

        # Horizontal margins
        if x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Left
            item.setCursor(Qt.SizeHorCursor)
        elif item.boundingRect().width() - x_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Right
            item.setCursor(Qt.SizeHorCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Left
            self.__margins_clicked &= ~self.MarginClicked.Right

        # Vertical margins
        if y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Top
            item.setCursor(Qt.SizeVerCursor)
        elif item.boundingRect().height() - y_pos <= self.resize_margins:
            self.__margins_clicked |= self.MarginClicked.Bottom
            item.setCursor(Qt.SizeVerCursor)
        else:
            self.__margins_clicked &= ~self.MarginClicked.Top
            self.__margins_clicked &= ~self.MarginClicked.Bottom

        if self.__margins_clicked == (self.MarginClicked.Left | self.MarginClicked.Top):
            item.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Left | self.MarginClicked.Bottom
        ):
            item.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Top
        ):
            item.setCursor(Qt.SizeBDiagCursor)

        if self.__margins_clicked == (
            self.MarginClicked.Right | self.MarginClicked.Bottom
        ):
            item.setCursor(Qt.SizeFDiagCursor)

        if self.__margins_clicked == self.MarginClicked.NoMargin:
            item.unsetCursor()
