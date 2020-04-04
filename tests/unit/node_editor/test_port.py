# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest

from dial_core.utils.exceptions import InvalidPortTypeError, PortNotConnectedError
from copy import deepcopy


def test_port_attributes(port_int_a):
    assert hasattr(port_int_a, "name")
    assert hasattr(port_int_a, "port_type")
    assert hasattr(port_int_a, "connections")
    assert hasattr(port_int_a, "node")
    assert hasattr(port_int_a, "allows_multiple_connections")


def test_ports_compatible(port_int_a, port_int_b, port_str):
    assert port_int_a.is_compatible_with(port_int_b)
    assert port_int_b.is_compatible_with(port_int_a)
    assert not port_int_a.is_compatible_with(port_str)


def test_connect_port_to_other(a_multi, b_multi):
    a_multi.connect_to(b_multi)

    assert a_multi in b_multi.connections
    assert b_multi in a_multi.connections

    assert len(a_multi.connections) == 1
    assert len(b_multi.connections) == 1


def test_connect_port_twice(a_multi, b_multi):
    a_multi.connect_to(b_multi)
    b_multi.connect_to(a_multi)

    assert a_multi in b_multi.connections
    assert b_multi in a_multi.connections

    # Check that ports aren't repeated
    assert len(a_multi.connections) == 1
    assert len(b_multi.connections) == 1


def test_connect_port_to_two_other_ports(a_multi, b_multi, c_multi):
    a_multi.connect_to(b_multi)
    a_multi.connect_to(c_multi)
    b_multi.connect_to(c_multi)

    assert a_multi in b_multi.connections
    assert a_multi in c_multi.connections
    assert b_multi in a_multi.connections
    assert b_multi in c_multi.connections
    assert c_multi in a_multi.connections
    assert c_multi in b_multi.connections

    assert len(a_multi.connections) == 2
    assert len(b_multi.connections) == 2
    assert len(c_multi.connections) == 2


def test_connect_port_to_two_other_ports_with_single_connection(
    a_single, b_single, c_single
):
    a_single.connect_to(b_single)

    assert a_single in b_single.connections
    assert b_single in a_single.connections

    a_single.connect_to(c_single)

    assert a_single not in b_single.connections
    assert b_single not in a_single.connections
    assert a_single in c_single.connections
    assert c_single in a_single.connections


def test_triangular_connection(a_multi, b_single, c_single):
    """
    Test this connection:
           b                     b
         //                       \\
        a          same as          a
         \\                       //
           c                     c
    Where a allows multiple connections (to b and c), but both b and c not.
    """
    a_multi.connect_to(b_single)
    a_multi.connect_to(c_single)

    assert b_single in a_multi.connections
    assert c_single in a_multi.connections

    # But then, if we try to connect b and c, the a connection will be cut
    #       b
    #   a   |
    #       c

    b_single.connect_to(c_single)

    assert c_single in b_single.connections
    assert b_single in c_single.connections
    assert b_single not in a_multi.connections
    assert c_single not in a_multi.connections


def test_connect_port_to_self(a_single):
    with pytest.raises(PortNotConnectedError):
        a_single.connect_to(a_single)


def test_connect_port_to_incompatible(port_int_a, port_str):
    with pytest.raises(InvalidPortTypeError):
        port_int_a.connect_to(port_str)


def test_disconnect_port_from_other(a_single, b_single):
    a_single.connect_to(b_single)

    b_single.disconnect_from(a_single)

    assert a_single not in b_single.connections
    assert b_single not in a_single.connections

    assert len(a_single.connections) == 0
    assert len(b_single.connections) == 0


def test_disconnect_port_twice(a_single, b_single):
    a_single.connect_to(b_single)

    b_single.disconnect_from(a_single)
    a_single.disconnect_from(b_single)

    assert a_single not in b_single.connections
    assert b_single not in a_single.connections

    assert len(a_single.connections) == 0
    assert len(b_single.connections) == 0


def test_clear_port_connections(a_multi, b_multi, c_multi):
    a_multi.connect_to(b_multi)
    a_multi.connect_to(c_multi)

    a_multi.clear_all_connections()

    assert len(a_multi.connections) == 0
    assert a_multi not in b_multi.connections
    assert a_multi not in c_multi.connections


def test_clone(a_single, b_single):
    a_single.connect_to(b_single)

    cloned_a_single = deepcopy(a_single)

    assert cloned_a_single.name == a_single.name
    assert cloned_a_single.port_type == a_single.port_type
    assert cloned_a_single.compatible_port_classes == a_single.compatible_port_classes
    assert (
        cloned_a_single.compatible_port_classes is not a_single.compatible_port_classes
    )
    assert len(cloned_a_single.connections) == 0


def test_pickable(a_single, b_single):
    a_single.connect_to(b_single)
    assert b_single in a_single.connections

    obj = pickle.dumps(a_single)
    loaded_a_single = pickle.loads(obj)

    test_port_attributes(loaded_a_single)
    assert loaded_a_single == a_single
    assert loaded_a_single.connections == a_single.connections

    loaded_b_single = list(loaded_a_single.connections)[0]
    assert loaded_b_single == b_single
    assert loaded_b_single.connections == b_single.connections
