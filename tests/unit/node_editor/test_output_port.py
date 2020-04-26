# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest

from dial_core.utils.exceptions import InvalidPortTypeError


def test_connect_to_incompatible_port(output_port_a, output_port_b):
    with pytest.raises(InvalidPortTypeError):
        output_port_a.connect_to(output_port_b)


def test_generate_output(output_port_a):
    output_port_a.set_generator_function(lambda: 1)

    assert output_port_a.generate_output() == 1


def test_generate_output_undefined(output_port_a):
    with pytest.raises(NotImplementedError):
        output_port_a.generate_output()


def test_set_invalid_generator_function(output_port_a):
    with pytest.raises(TypeError):
        output_port_a.set_generator_function(None)


def test_send(input_port_a, output_port_a):
    input_port_a.__test_value = 0

    def change_port_test_value_to(port, x):
        port.__test_value = x

    input_port_a.connect_to(output_port_a)

    output_port_a.set_generator_function(lambda: 10)
    input_port_a.set_processor_function(
        lambda x: change_port_test_value_to(input_port_a, x)
    )

    output_port_a.send()
    assert input_port_a.__test_value == 10


def test_pickable(output_port_a, input_port_a):
    output_port_a.connect_to(input_port_a)
    assert input_port_a in output_port_a.connections

    obj = pickle.dumps(output_port_a)
    loaded_output_port_a = pickle.loads(obj)

    assert loaded_output_port_a == output_port_a
    assert loaded_output_port_a._generator_function == output_port_a._generator_function

    assert loaded_output_port_a.connections == output_port_a.connections
    assert input_port_a in loaded_output_port_a.connections
