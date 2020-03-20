# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dependency_injector import providers

from dial_core.node_editor import Node


class TalkNode(Node):
    def __init__(self, say: str = "foo"):
        self.say = say


def test_register_node(node_registry):
    node_registry.register_node("Talk Node", TalkNode)

    assert "Talk Node" in node_registry.nodes

    assert isinstance(node_registry.nodes["Talk Node"], providers.Factory)


def test_register_factory(node_registry):
    node_factory = providers.Factory(TalkNode)

    node_registry.register_node("Talk Node", node_factory)

    assert "Talk Node" in node_registry.nodes

    node = node_registry.get_node("Talk Node")
    assert isinstance(node, TalkNode)


def test_unregister_node(node_registry):
    node_registry.register_node("Talk Node", TalkNode)

    assert "Talk Node" in node_registry.nodes

    node_registry.unregister_node("Talk Node")

    assert "Talk Node" not in node_registry.nodes


def test_unregister_unrecognized_node(node_registry):
    node_registry.unregister_node("This Node Does Not Exists")


def test_register_invalid_node(node_registry):
    # With wrong types
    with pytest.raises(TypeError):
        node_registry.register_node("Foo", int)

    # With wrong objects
    with pytest.raises(TypeError):
        node_registry.register_node("Foo", "test")

    # With None
    with pytest.raises(TypeError):
        node_registry.register_node("Foo", None)


def test_get_node(node_registry):
    node_registry.register_node("Foo Node", TalkNode, say="foo")
    node_registry.register_node("Bar Node", TalkNode, say="bar")

    foo_node = node_registry.get_node("Foo Node")

    assert isinstance(foo_node, TalkNode)
    assert foo_node.say == "foo"

    foo_node_2 = node_registry.get_node("Foo Node")

    # The two instances are different
    assert foo_node is not foo_node_2

    bar_node = node_registry.get_node("Bar Node")

    assert isinstance(bar_node, TalkNode)


def test_get_inexistent_node(node_registry):
    with pytest.raises(KeyError):
        node_registry.get_node("This Node Does Not Exists")


def test_clear_nodes(node_registry):
    assert len(node_registry.nodes) == 0

    node_registry.register_node("Talk Node", TalkNode)

    assert len(node_registry.nodes) != 0

    node_registry.clear()

    assert len(node_registry.nodes) == 0
