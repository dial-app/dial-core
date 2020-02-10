# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Base class for the Node system"""


from .graphics_node import GraphicsNode


class Node:
    def __init__(self, scene, title="Undefined Node"):
        self.scene = scene

        self.title = title

        self.grNode = GraphicsNode(self, self.title)

        self.scene.addNode(self)

        self.inputs = []
        self.outpus = []
