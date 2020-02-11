# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum

from .graphics_socket import GraphicsSocket


class Socket:
    class Position(Enum):
        LeftTop = 1
        # LeftBottom = 2
        RightTop = 3
        # RightBottom = 4

    def __init__(self, position=Position.LeftTop):
        self.position = position

        self.index = 0
        self.node = None
        self.graphics_socket = GraphicsSocket(self)

        self.edge = None

    def set_connected_edge(self, edge=None):
        self.edge = edge
