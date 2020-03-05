# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_scene_nodes(scene):
    assert hasattr(scene, "nodes")


def test_add_node(scene, node_a):
    assert not scene.nodes

    scene.add_node(node_a)

    assert node_a in scene.nodes


def test_eq(scene):
    assert scene == scene
    assert not scene == 123
