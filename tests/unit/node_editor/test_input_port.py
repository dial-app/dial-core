# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest

from dial_core.utils.exceptions import InvalidPortTypeError, PortNotConnectedError


def test_port_connected_to(input_port_a, output_port_a):
    assert input_port_a.port_connected_to is None

    input_port_a.connect_to(output_port_a)

    assert input_port_a.port_connected_to is output_port_a


def test_connect_to_incompatible_port(input_port_a, input_port_b):
    with pytest.raises(InvalidPortTypeError):
        input_port_a.connect_to(input_port_b)


def test_set_invalid_processor_function(input_port_a):
    with pytest.raises(TypeError):
        input_port_a.set_processor_function("a")


def test_receive(input_port_a, output_port_a):
    output_port_a.set_generator_function(lambda: 5)

    input_port_a.connect_to(output_port_a)

    assert input_port_a.receive() == 5


def test_receive_processing(input_port_a, output_port_a):
    output_port_a.set_generator_function(lambda: 5)
    input_port_a.set_processor_function(lambda x: x * 2)

    input_port_a.connect_to(output_port_a)

    assert output_port_a.generate_output() == 5
    assert input_port_a.process_input(5) == 10
    assert input_port_a.receive() == 10


def test_receive_not_connected(input_port_a):
    with pytest.raises(PortNotConnectedError):
        input_port_a.receive()


def test_process_input_override_to_default(input_port_a):
    assert input_port_a.process_input(5) == 5

    input_port_a.set_processor_function(lambda x: x * 2)
    assert input_port_a.process_input(5) == 10

    input_port_a.set_processor_function(None)
    assert input_port_a.process_input(5) == 5


def test_input_port_attributes(input_port_a):
    assert hasattr(input_port_a, "name")
    assert hasattr(input_port_a, "port_type")
    assert hasattr(input_port_a, "_processor_function")


def test_pickable(input_port_a, output_port_a):
    input_port_a.connect_to(output_port_a)

    assert output_port_a in input_port_a.connections

    obj = pickle.dumps(input_port_a)
    loaded_input_port_a = pickle.loads(obj)

    assert loaded_input_port_a == input_port_a

    assert loaded_input_port_a.connections == input_port_a.connections
    assert output_port_a in loaded_input_port_a.connections
