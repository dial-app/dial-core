# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial.node_editor import Node, Port


@pytest.fixture
def node_a():
    """Empty node a. Allows multiple connections to different ports. """
    return Node(title="a")


def node_b():
    """Empty node b. Allows multiple connections to different ports. """
    return Node(title="b")


def test_title(node_a):
    assert node_a.title == "a"


def test_add_input(node_a):
    my_input_port = Port()
    node_a.add_input("port", my_input_port)

    assert node_a.inputs["port"] == my_input_port
    assert my_input_port not in node_a.outputs.values()


def test_add_output(node_a):
    my_output_port = Port()
    node_a.add_output("port", my_output_port)

    assert node_a.outputs["port"] == my_output_port
    assert my_output_port not in node_a.inputs.values()


def test_remove_input(node_a):
    my_input_port = Port()
    node_a.add_input("port", my_input_port)

    node_a.remove_input("port")
    assert my_input_port not in node_a.inputs


def test_remove_output(node_a):
    my_output_port = Port()
    node_a.add_output("port", my_output_port)

    node_a.remove_output("port")
    assert my_output_port not in node_a.outputs
