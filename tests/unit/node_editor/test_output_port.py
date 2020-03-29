# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


def test_get_output_value(output_port_a):
    def get_num_1():
        return 1

    output_port_a.set_generator_function(get_num_1)

    assert output_port_a.generate_output() == 1


def test_connect_to_incompatible_node(output_port_a, output_port_b):
    with pytest.raises(ValueError):
        output_port_a.connect_to(output_port_b)


def test_pickable(output_port_a, input_port_a):
    output_port_a.connect_to(input_port_a)
    assert input_port_a in output_port_a.connections

    obj = pickle.dumps(output_port_a)
    loaded_output_port_a = pickle.loads(obj)

    assert loaded_output_port_a == output_port_a
    assert loaded_output_port_a._generator_function == output_port_a._generator_function

    assert loaded_output_port_a.connections == output_port_a.connections
    assert input_port_a in loaded_output_port_a.connections
