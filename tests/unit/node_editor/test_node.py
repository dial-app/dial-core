# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from copy import deepcopy

import pytest


def test_title(node_a):
    assert hasattr(node_a, "title")


def test_set_title(node_a):
    node_a.title = "b"
    assert node_a.title == "b"


def test_inner_widget(node_a):
    assert hasattr(node_a, "inner_widget")


def test_add_input_port(node_a, a_single):
    node_a.add_input_port(a_single)

    assert node_a.inputs["a_single"] == a_single
    assert a_single not in node_a.outputs.values()

    assert a_single.node is node_a


def test_add_output_port(node_a, a_single):
    node_a.add_output_port(a_single)

    assert node_a.outputs["a_single"] == a_single
    assert a_single not in node_a.inputs.values()

    assert a_single.node is node_a


def test_remove_input_port(node_a, a_single):
    node_a.add_input_port(a_single)

    node_a.remove_input_port("a_single")
    assert a_single not in node_a.inputs

    assert a_single.node is None


def test_remove_inexistent_input_port(node_a, a_single):
    with pytest.raises(ValueError):
        node_a.remove_input_port("not_exists")


def test_remove_output_port(node_a, a_single):
    node_a.add_output_port(a_single)

    node_a.remove_output_port("a_single")
    assert a_single not in node_a.outputs

    assert a_single.node is None


def test_remove_inexistent_output_port(node_a, a_single):
    with pytest.raises(ValueError):
        node_a.remove_output_port("not_exists")


def test_remove_connected_port(node_a, a_single, b_single):
    a_single.connect_to(b_single)

    node_a.add_input_port(a_single)

    assert a_single in b_single.connections
    assert b_single in a_single.connections

    node_a.remove_input_port("a_single")

    assert a_single not in b_single.connections
    assert b_single not in a_single.connections


def test_node_connect_to_node(node_a, node_b, a_single, b_single):
    node_a.add_output_port(a_single)
    node_b.add_input_port(b_single)

    node_a.outputs["a_single"].connect_to(node_b.inputs["b_single"])

    # Assert the two ports are connected
    assert a_single in b_single.connections
    assert b_single in a_single.connections


def test_node_connect_to_inexistent(node_a, node_b, a_single):
    node_a.add_output_port(a_single)

    with pytest.raises(KeyError):
        node_a.outputs["a_single"].connect_to(node_b.inputs["doesnt_exists"])


def test_node_eq(node_a):
    copy_node_a = deepcopy(node_a)

    assert node_a == copy_node_a


def test_pickable(node_a, input_port_a, output_port_a):
    node_a.add_input_port(input_port_a)
    node_a.add_output_port(output_port_a)

    assert input_port_a in node_a.inputs.values()
    assert output_port_a in node_a.outputs.values()

    obj = pickle.dumps(node_a)
    loaded_node_a = pickle.loads(obj)

    assert loaded_node_a == node_a
    assert input_port_a in loaded_node_a.inputs.values()
    assert output_port_a in loaded_node_a.outputs.values()
