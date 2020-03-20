# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

from dial_core.node_editor import Node, Scene


def test_save_and_load_scene():
    node_a = Node(title="a")
    node_a.add_output_port("out", port_type=int)

    node_b = Node(title="b")
    node_b.add_input_port("in", port_type=int)

    node_a.outputs["out"].connect_to(node_b.inputs["in"])

    scene = Scene()
    scene.add_node(node_a)
    scene.add_node(node_b)

    obj = pickle.dumps(scene)
    loaded_scene = pickle.loads(obj)

    loaded_node_a = loaded_scene.nodes[0]
    loaded_node_b = loaded_scene.nodes[1]

    assert node_a == loaded_node_a
    assert node_b == loaded_node_b

    assert node_b.inputs["in"] in node_a.outputs["out"].connections
    assert node_a.outputs["out"] in node_b.inputs["in"].connections
