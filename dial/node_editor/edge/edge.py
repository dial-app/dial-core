# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from enum import Enum

from .graphics_edge import GraphicsEdgeBezier, GraphicsEdgeDirect


class Edge:
    def __init__(self, start_socket, end_socket, edge_type=GraphicsEdgeDirect):
        self.scene = None

        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphics_edge = edge_type(self)

        print(edge_type)
