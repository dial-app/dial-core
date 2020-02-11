# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .node import Node
from .port import Port

__all__ = ["Node"]

"""
scene = NodeEditorScene()
view = NodeEditorView()
view.setScene(scene)

dataset_node = DatasetsNode()
training_node = ModelsNode()

dataset_node.outputs["train"].connect_to(training_node.input["dataset"])

dataset_node.outputs["train"].disconnect_from(training_node.input["dataset"])

class Node:
    def __init__(self, title):
        self.title = title

        self.inputs = {}
        self.outputs = {}


class Port:
    def __init__(self, allows_multiple_connections=False)
        self.__connected_to = set() # Avoid port repetition

        self.accepts_multiple_connections = accepts_multiple_connections

    def connect_to(self, port: Port):
        # Avoid connect a port to itself
        if port is self:
            return

        # Two way connection to ensure that both ports know the connection
        if self.accepts_multiple_connections:
            self.__connected_to.add(port)
            port.connect_to(self)
        else:
            pass


    def disconnect(self, port: Port):







scene.addNode(dataset_node)
scene.addNode(training_node)


"""
