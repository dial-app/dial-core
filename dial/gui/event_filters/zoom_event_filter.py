# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import TYPE_CHECKING

from PySide2.QtCore import QEvent, QObject

if TYPE_CHECKING:
    from PySide2.QtWidgets import QGraphicsView
    from PySide2.QtGui import QWheelEvent


class ZoomEventFilter(QObject):
    """The ZoomEventFilter class provides an easy implementation of a zoom movement for
    a QGraphicsView object.

    This filter only works with a QGraphicsView object.

    Attributes:
        scale_factor_increment: Percentage incremented on each zoom step.

    Examples:
        view = QGraphicsView()
        zoom_event_filter = ZoomEventFilter()

        view.installEventFilter(zoom_event_filter)

        # Now the `view` can be zoomed using the mouse.
    """

    def __init__(self, parent: "QObject" = None):
        super().__init__(parent)

        self.scale_factor_increment = 0.2

    def eventFilter(self, obj: "QObject", event: "QEvent") -> bool:
        """Intercepts events emitted by `obj`. In this case, implements a zoom effect
        when the mouse wheel is moved up/down.

        This filter only works with a QGraphicsView object.

        Args:
            obj: The object (QGraphicsView) to pan.
            event: The generated event.

        Returns:
            if the event should be filtered out or not (Stopping it being handled by
            other objects).
        """
        if event.type() == QEvent.Wheel:
            return self.__zoom_view(obj, event)

        return super().eventFilter(obj, event)

    def __zoom_view(self, view: "QGraphicsView", event: "QWheelEvent") -> bool:
        """Zooms in/out the view using the mouse wheel.
        """
        if event.delta() > 0:
            view.scale(
                1.0 + self.scale_factor_increment, 1.0 + self.scale_factor_increment
            )
        else:
            view.scale(
                1.0 - self.scale_factor_increment, 1.0 - self.scale_factor_increment
            )

        return True
