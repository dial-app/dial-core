# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from .node import Node
from .port import Port

__all__ = ["Node"]

"""
scene = NodeEditorScene()
view = NodeEditorView()
view.setScene(scene)

node_a = Node(title="a")
node_b = Node(title="b")

dataset_node.outputs["train"].connect_to(training_node.input["dataset"])

dataset_node.outputs["train"].disconnect_from(training_node.input["dataset"])

scene.addNode(dataset_node)
scene.addNode(training_node)
"""
