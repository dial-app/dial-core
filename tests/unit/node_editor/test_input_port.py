# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_port_connected_to(input_port_a, output_port_a):

    assert input_port_a.port_connected_to is None

    input_port_a.connect_to(output_port_a)

    assert input_port_a.port_connected_to is output_port_a
