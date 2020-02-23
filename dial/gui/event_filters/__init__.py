from .panning_event_filter import PanningEventFilter
from .resizable_item_event_filter import ResizableItemEventFilter
from .zoom_event_filter import ZoomEventFilter

"""This package includes some common event filters: Classes that implements new sets of
movements and operations on an object.

For example, by installing a `ZoomEventFilter` object on a QGrapQGraphicsView, you will
be able to zoom in/out the view using the mouse.
"""

__all__ = ["PanningEventFilter", "ZoomEventFilter", "ResizableItemEventFilter"]
