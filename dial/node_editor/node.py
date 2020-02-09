# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""

from typing import Any

from PySide2.QtCore import QRectF, Qt
from PySide2.QtGui import QPainter, QPainterPath, QPen
from PySide2.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget


class Node(QGraphicsItem):
    """Base class for all the nodes.

    Attributes:
        _id: Unique identifier of the node.
    """

    def __init__(self):
        pass
