# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum

from .graphics_socket import GraphicsSocket


class Socket:
    class Position(Enum):
        LeftTop = 1
        # LeftBottom = 2
        RightTop = 3
        # RightBottom = 4

    def __init__(self, socket_type=1, position=Position.LeftTop):
        self.position = position
        self.index = 0
        self.socket_type = socket_type

        self.node = None
        self.edge = None

        self.graphics_socket = GraphicsSocket(self)

    def set_connected_edge(self, edge=None):
        self.edge = edge
