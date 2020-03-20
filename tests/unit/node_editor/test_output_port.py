# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


def test_get_output_value(output_port_a):
    def get_num_1():
        return 1

    output_port_a.output_generator = get_num_1

    assert output_port_a.get_output_value() == 1


def test_get_output_value_not_set(output_port_a):
    with pytest.raises(AttributeError):
        output_port_a.get_output_value()


def test_connect_to_incompatible_node(output_port_a, output_port_b):
    with pytest.raises(ValueError):
        output_port_a.connect_to(output_port_b)


def test_pickable(output_port_a, input_port_a):
    output_port_a.connect_to(input_port_a)
    assert input_port_a in output_port_a.connections

    obj = pickle.dumps(output_port_a)
    loaded_output_port_a = pickle.loads(obj)

    assert loaded_output_port_a == output_port_a
    assert loaded_output_port_a.output_generator == output_port_a.output_generator

    assert loaded_output_port_a.connections == output_port_a.connections
    assert input_port_a in loaded_output_port_a.connections
