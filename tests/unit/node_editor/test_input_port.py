# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


def test_port_connected_to(input_port_a, output_port_a):

    assert input_port_a.port_connected_to is None

    input_port_a.connect_to(output_port_a)

    assert input_port_a.port_connected_to is output_port_a


def test_input_port_attributes(input_port_a):
    assert hasattr(input_port_a, "name")
    assert hasattr(input_port_a, "port_type")


def test_connect_to_incompatible_node(input_port_a, input_port_b):
    with pytest.raises(ValueError):
        input_port_a.connect_to(input_port_b)


def test_pickable(input_port_a, output_port_a):
    input_port_a.connect_to(output_port_a)

    assert output_port_a in input_port_a.connections

    obj = pickle.dumps(input_port_a)
    loaded_input_port_a = pickle.loads(obj)

    assert loaded_input_port_a == input_port_a

    assert loaded_input_port_a.connections == input_port_a.connections
    assert output_port_a in loaded_input_port_a.connections
