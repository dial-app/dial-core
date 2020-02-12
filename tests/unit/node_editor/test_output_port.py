# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


import pytest


def test_get_output_value(output_port_a):
    def get_num_1():
        return 1

    output_port_a.output_generator = get_num_1

    assert output_port_a.get_output_value() == 1


def test_get_output_value_not_set(output_port_a):
    with pytest.raises(AttributeError):
        output_port_a.get_output_value()
