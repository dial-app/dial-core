# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from copy import deepcopy


def test_scene_nodes(scene):
    assert hasattr(scene, "nodes")


def test_add_node(scene, node_a):
    assert not scene.nodes

    scene.add_node(node_a)

    assert node_a in scene


def test_remove_node(scene, node_a, node_b):
    scene.add_node(node_a)
    scene.add_node(node_b)

    assert node_a in scene
    assert node_b in scene

    scene.remove_node(node_a)

    assert node_a not in scene
    assert node_b in scene

    # Removing nodes that aren't registered on the scene doesn't raise any exception
    scene.remove_node(node_a)


def test_duplicate_nodes(scene, node_a, node_b):
    node_a.add_output_port(name="value", port_type=int)
    node_b.add_input_port(name="value", port_type=int)
    # node_a.outputs["value"].connect_to(node_b.inputs["value"])
    node_b.inputs["value"].connect_to(node_a.outputs["value"])

    new_nodes = scene.duplicate_nodes([node_a, node_b])

    new_node_a = new_nodes[0]
    new_node_b = new_nodes[1]

    print(new_node_a.outputs["value"].connections)

    assert new_node_a is not node_a
    assert new_node_b is not node_b

    assert len(new_node_a.outputs["value"].connections) == 1
    assert len(new_node_b.inputs["value"].connections) == 1

    assert new_node_b.inputs["value"] in new_node_a.outputs["value"].connections
    assert new_node_a.outputs["value"] in new_node_b.inputs["value"].connections

    new_new_nodes = scene.duplicate_nodes(new_nodes)
    print("New new nodes", new_new_nodes)

    new_new_node_a = new_new_nodes[0]
    new_new_node_b = new_new_nodes[1]

    print(new_new_node_a.outputs["value"].connections)

    assert new_new_node_a is not node_a
    assert new_new_node_b is not node_b

    assert len(new_new_node_a.outputs["value"].connections) == 1
    assert len(new_new_node_b.inputs["value"].connections) == 1

    assert new_new_node_b.inputs["value"] in new_new_node_a.outputs["value"].connections
    assert new_new_node_a.outputs["value"] in new_new_node_b.inputs["value"].connections


def test_eq(scene):
    copy_scene = deepcopy(scene)
    assert scene == copy_scene


def test_pickable(scene, node_a, node_b, input_port_a, output_port_a):
    input_port_a.connect_to(output_port_a)

    node_b.add_port(input_port_a)
    node_a.add_port(output_port_a)

    scene.add_node(node_a)
    scene.add_node(node_b)

    obj = pickle.dumps(scene)
    loaded_scene = pickle.loads(obj)

    assert loaded_scene == scene

    assert (
        loaded_scene.nodes[1].inputs["a"]
        in loaded_scene.nodes[0].outputs["a"].connections
    )
