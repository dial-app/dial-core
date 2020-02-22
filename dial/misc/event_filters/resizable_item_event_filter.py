# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum, Flag, auto

from PySide2.QtCore import QEvent, QObject, QRectF, Qt
from PySide2.QtWidgets import QGraphicsItem


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

        self.start_resizing_x = 0
        self.start_resizing_y = 0

        self.button_used_for_resizing = Qt.LeftButton

    @property
    def state(self) -> "ResizableItemEventFilter.State":
        return self.__state

    def is_resizing(self) -> bool:
        return self.__state == self.State.Resizing

    def eventFilter(self, item: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.GraphicsSceneHoverMove:  # TODO: Change
            self.__adjust_margins_inside_cursor(item, event)
            return True

        if self.__resizing_button_clicked(event) and self.is_inside_resize_margins(
            item, event
        ):
            self.__start_resizing_item(item, event)
            return True

        if event.type() == QEvent.GraphicsSceneMouseMove and self.is_resizing():
            self.__resize_item(item, event)
            return True

        if self.__resizing_button_released(event) and self.is_inside_resize_margins(
            item, event
        ):
            self.__stop_resizing_item(item, event)
            return True

        return super().eventFilter(item, event)

    def __resizing_button_clicked(self, event: QEvent) -> bool:
        return (
            event.type() == QEvent.GraphicsSceneMousePress
            and event.button() == self.button_used_for_resizing
        )

    def __resizing_button_released(self, event: QEvent) -> bool:
        return (
            event.type() == QEvent.GraphicsSceneMouseRelease
            and event.button() == self.button_used_for_resizing
        )

    def __start_resizing_item(self, item: QGraphicsItem, event: QEvent):
        self.__state = self.State.Resizing

        self.start_resize_pos = event.scenePos()
        self.start_item_pos = item.pos()
        self.start_geometry = item.proxy_widget.geometry()

    def __resize_item(self, item: QGraphicsItem, event: QEvent):
        diff = self.start_resize_pos - event.scenePos()

        new_x = 0
        new_y = 0
        new_w = 0
        new_h = 0

        if self.__margins_clicked & self.MarginClicked.Left:
            new_x = min(-diff.x(), 0)
            new_w = diff.x()

        if self.__margins_clicked & self.MarginClicked.Right:
            new_w = -diff.x()

        if self.__margins_clicked & self.MarginClicked.Top:
            new_y = min(-diff.y(), 0)
            new_h = diff.y()

        if self.__margins_clicked & self.MarginClicked.Bottom:
            new_h = -diff.y()

        item.prepareGeometryChange()

        item.proxy_widget.setGeometry(self.start_geometry.adjusted(0, 0, new_w, new_h))
        item.setPos(self.start_item_pos.x() + new_x, self.start_item_pos.y() + new_y)

        item.recalculateGeometry()

    def __stop_resizing_item(self, item: QGraphicsItem, event: QEvent):
        self.__state = self.State.Idle

    def is_inside_resize_margins(self, item: QGraphicsItem, event: QEvent) -> bool:
        return self.__margins_clicked != self.MarginClicked.NoMargin

    def __adjust_margins_inside_cursor(self, item: QGraphicsItem, event: QEvent):
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
