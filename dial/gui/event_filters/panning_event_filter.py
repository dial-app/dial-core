# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum
from typing import TYPE_CHECKING

from PySide2.QtCore import QEvent, QObject, Qt
from PySide2.QtGui import QGuiApplication, QMouseEvent

if TYPE_CHECKING:
    from PySide2.QtWidgets import QGraphicsView


class PanningEventFilter(QObject):
    """The PanningEventFilter class provides an easy implementation of a panning
    movement for a QGraphicsView object.

    Important:
        This filter only works with a QGraphicsView object.

    Attributes:
        state: The state of the movement (Panning or not).
        button_used_for_panning: The button that must be pressed and dragged for panning
        the view.

    Examples:
        view = QGraphicsView()
        panning_event_filter = PanningEventFilter()

        view.installEventFilter(panning_event_filter)

        # Now the `view` can be panned using the mouse.
    """

    class State(Enum):
        Idle = 0
        Panning = 1

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.__state = self.State.Idle

        self.__panning_start_x = 0
        self.__panning_start_y = 0

        self.button_used_for_panning = Qt.MiddleButton

    def is_panning(self) -> bool:
        """Checks if the view is currently being panned."""
        return self.__state == self.State.Panning

    def eventFilter(self, obj: "QObject", event: "QEvent") -> bool:
        """Intercepts events emitted by `obj`. Implements a panning effect when the mouse
        is dragged throughout the scene.

        This filter only works with a QGraphicsView object.

        Args:
            obj: The object (QGraphicsView) to pan.
            event: The generated event.

        Returns:
            If the event should be filtered out or not (Stopping it being handled by
            other objects).
        """
        if self.__panning_button_clicked(event):
            self.__start_panning_view(obj, event)
            return True

        if event.type() == QEvent.MouseMove and self.is_panning():
            self.__pan_view(obj, event)
            return True

        if self.__panning_button_released(event):
            self.__stop_panning_view(obj, event)
            return True

        return super().eventFilter(obj, event)

    def __panning_button_clicked(self, event: "QMouseEvent") -> bool:
        """Checks if the button defined as the "panning button" was clicked.

        This starts the panning movement.
        """
        return (
            event.type() == QMouseEvent.MouseButtonPress
            and event.button() == self.button_used_for_panning
        )

    def __panning_button_released(self, event: "QMouseEvent") -> bool:
        """Checks if the button defined as the "panning button" was released.

        This ends the panning movement.
        """
        return (
            event.type() == QMouseEvent.MouseButtonRelease
            and event.button() == self.button_used_for_panning
        )

    def __start_panning_view(self, view: "QGraphicsView", event: "QMouseEvent"):
        """Responds to the event of start panning the view.

        Changes the mouse icon to a dragging hand, and saves the last clicked position.
        This is used for calculating the mouse displacement.

        Args:
            view: The QGraphicsView object to pan.
            event: Mouse event.
        """
        QGuiApplication.setOverrideCursor(Qt.ClosedHandCursor)

        self.__panning_start_x = event.x()
        self.__panning_start_y = event.y()

        self.__state = self.State.Panning

    def __pan_view(self, view: "QGraphicsView", event: "QMouseEvent"):
        """Pans the view using the mouse movement.

        The scrollbars are moved along the view (They're disabled by default, but if
        they were enabled, the scrollbars would be scrolled along the view
        displacement).

        Args:
            view: The QGraphicsView object to pan.
            event: Generated mouse event.
        """
        # Move view by using the scrollbars
        view.horizontalScrollBar().setValue(
            view.horizontalScrollBar().value() - (event.x() - self.__panning_start_x)
        )

        view.verticalScrollBar().setValue(
            view.verticalScrollBar().value() - (event.y() - self.__panning_start_y)
        )

        # Set new "last panning values"
        self.__panning_start_x = event.x()
        self.__panning_start_y = event.y()

    def __stop_panning_view(self, view: "QGraphicsView", event: "QMouseEvent"):
        """Responds to the event of start dragging the view for panning it.

        Changes the mouse icon back to the default icon.

        Args:
            view: The QGraphicsView object to pan.
            event: Mouse event.
        """
        QGuiApplication.restoreOverrideCursor()

        self.__state = self.State.Idle
