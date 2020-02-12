# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Type

from dial.node_editor import Port


class InputPort(Port):
    def __init__(self, port_type: Type):
        super().__init__(port_type, allows_multiple_connections=False)

    def send(self):
        pass
