# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest
from dependency_injector import providers

from dial_core.node_editor import Node


class TalkNode(Node):
    def __init__(self, say: str = "foo"):
        self.say = say


def test_register_node(node_factory):
    node_factory.register_node("Talk Node", TalkNode)

    assert "Talk Node" in node_factory.nodes

    assert isinstance(node_factory.nodes["Talk Node"], providers.Factory)


def test_register_invalid_node(node_factory):
    # With wrong types
    with pytest.raises(TypeError):
        node_factory.register_node("Foo", int)

    # With wrong objects
    with pytest.raises(TypeError):
        node_factory.register_node("Foo", "test")

    # With None
    with pytest.raises(TypeError):
        node_factory.register_node("Foo", None)


def test_get_node(node_factory):
    node_factory.register_node("Foo Node", TalkNode, say="foo")
    node_factory.register_node("Bar Node", TalkNode, say="bar")

    foo_node = node_factory.get_node("Foo Node")

    assert isinstance(foo_node, TalkNode)
    assert foo_node.say == "foo"

    foo_node_2 = node_factory.get_node("Foo Node")

    # The two instances are different
    assert foo_node is not foo_node_2

    bar_node = node_factory.get_node("Bar Node")

    assert isinstance(bar_node, TalkNode)


def test_get_inexistent_node(node_factory):
    with pytest.raises(KeyError):
        node_factory.get_node("This Node Does Not Exists")


def test_clear_nodes(node_factory):
    assert len(node_factory.nodes) == 0

    node_factory.register_node("Talk Node", TalkNode)

    assert len(node_factory.nodes) != 0

    node_factory.clear()

    assert len(node_factory.nodes) == 0
