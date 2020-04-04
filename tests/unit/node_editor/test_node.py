# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from copy import deepcopy

import pytest

from dial_core.node_editor import Node
from dial_core.utils.exceptions import InvalidPortTypeError


class InnerWidget:
    def __init__(self):
        self.value = 100


def test_title(node_a):
    assert hasattr(node_a, "title")


def test_set_title(node_a):
    node_a.title = "b"
    assert node_a.title == "b"


def test_inner_widget(node_a):
    assert hasattr(node_a, "inner_widget")


def test_add_input_port(node_a):
    input_port = node_a.add_input_port(name="input_port", port_type=int)

    assert node_a.inputs["input_port"] == input_port
    assert input_port in node_a.inputs.values()
    assert input_port not in node_a.outputs.values()

    assert input_port.node is node_a


def test_add_output_port(node_a):
    output_port = node_a.add_output_port(name="output_port", port_type=int)

    assert node_a.outputs["output_port"] == output_port
    assert output_port in node_a.outputs.values()
    assert output_port not in node_a.inputs.values()

    assert output_port.node is node_a


def test_add_port(node_a, input_port_a, output_port_a):
    node_a.add_port(input_port_a)
    node_a.add_port(output_port_a)

    assert node_a.inputs["a"] == input_port_a
    assert node_a.outputs["a"] == output_port_a

    assert input_port_a.node is node_a
    assert output_port_a.node is node_a


def test_add_not_port(node_a):
    with pytest.raises(InvalidPortTypeError):
        node_a.add_port("foo")


def test_remove_input_port(node_a, input_port_a):
    node_a.add_port(input_port_a)

    node_a.remove_input_port("a")
    assert input_port_a not in node_a.inputs

    assert input_port_a.node is None


def test_remove_inexistent_input_port(node_a):
    with pytest.raises(ValueError):
        node_a.remove_input_port("not_exists")


def test_remove_output_port(node_a, output_port_a):
    node_a.add_port(output_port_a)

    node_a.remove_output_port("a")
    assert output_port_a not in node_a.outputs

    assert output_port_a.node is None


def test_remove_inexistent_output_port(node_a):
    with pytest.raises(ValueError):
        node_a.remove_output_port("not_exists")


def test_remove_connected_port(node_a, input_port_a, output_port_a):
    input_port_a.connect_to(output_port_a)

    node_a.add_port(input_port_a)

    assert input_port_a in output_port_a.connections
    assert output_port_a in input_port_a.connections

    node_a.remove_input_port("a")

    assert input_port_a not in output_port_a.connections
    assert output_port_a not in input_port_a.connections


def test_node_connect_to_node(node_a, node_b, input_port_a, output_port_a):
    node_a.add_port(output_port_a)
    node_b.add_port(input_port_a)

    node_a.outputs["a"].connect_to(node_b.inputs["a"])

    # Assert the two ports are connected
    assert input_port_a in output_port_a.connections
    assert output_port_a in input_port_a.connections


def test_node_connect_to_inexistent(node_a, node_b, output_port_a):
    node_a.add_port(output_port_a)

    with pytest.raises(KeyError):
        node_a.outputs["a"].connect_to(node_b.inputs["doesnt_exists"])


def test_deepcopy():
    node_a = Node(title="a", inner_widget=InnerWidget())
    node_a.add_input_port("inputport", port_type=str)
    node_a.add_output_port("value", port_type=int)

    node_b = Node(title="b")
    node_b.add_input_port("value", port_type=int)

    node_a.outputs["value"].connect_to(node_b.inputs["value"])

    node_a_clone = deepcopy(node_a)

    assert node_a_clone.inner_widget is not node_a.inner_widget
    assert len(node_a_clone.inputs) == 1
    assert len(node_a_clone.outputs) == 1

    # Only connections are not copied
    assert len(node_a_clone.outputs["value"].connections) == 0


def test_node_eq(node_a):
    copy_node_a = deepcopy(node_a)

    assert node_a == copy_node_a


def test_pickable(node_a, input_port_a, output_port_a):
    node_a.add_port(input_port_a)
    node_a.add_port(output_port_a)

    assert input_port_a in node_a.inputs.values()
    assert output_port_a in node_a.outputs.values()

    obj = pickle.dumps(node_a)
    loaded_node_a = pickle.loads(obj)

    assert loaded_node_a == node_a
    assert input_port_a in loaded_node_a.inputs.values()
    assert output_port_a in loaded_node_a.outputs.values()
