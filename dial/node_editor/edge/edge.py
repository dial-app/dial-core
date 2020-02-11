# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .graphics_edge import GraphicsEdgeDirect


class Edge:
    def __init__(self, start_socket, end_socket, edge_type=GraphicsEdgeDirect):
        self.start_socket = start_socket
        self.end_socket = end_socket

        self.graphics_edge = edge_type(self)

    def remove_from_socket(self):
        if self.start_socket:
            self.start_socket.edge = None

        if self.end_socket:
            self.end_socket.edge = None

        self.start_socket = None
        self.end_socket = None

    def remove(self):
        self.remove_from_socket()
