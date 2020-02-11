# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial.node_editor import Port


@pytest.fixture
def a():
    """Empty port a. Allows multiple connections to different ports. """
    return Port(port_type=int)


@pytest.fixture
def b():
    """Empty port b. Allows multiple connections to different ports. """
    return Port(port_type=int)


@pytest.fixture
def c():
    """Empty port c. Allows multiple connections to different ports. """
    return Port(port_type=int)


def test_ports_compatible():
    p1 = Port(port_type=int)
    p2 = Port(port_type=int)
    p3 = Port(port_type=str)

    assert p1.is_compatible_with(p2)
    assert p2.is_compatible_with(p1)
    assert not p1.is_compatible_with(p3)


def test_connect_port_to_other(a, b):
    a.connect_to(b)

    assert a in b.connections
    assert b in a.connections

    assert len(a.connections) == 1
    assert len(b.connections) == 1


def test_connect_port_twice(a, b):
    a.connect_to(b)
    b.connect_to(a)

    assert a in b.connections
    assert b in a.connections

    # Check that ports aren't repeated
    assert len(a.connections) == 1
    assert len(b.connections) == 1


def test_connect_port_to_two_other_ports(a, b, c):
    a.connect_to(b)
    a.connect_to(c)
    b.connect_to(c)

    assert a in b.connections
    assert a in c.connections
    assert b in a.connections
    assert b in c.connections
    assert c in a.connections
    assert c in b.connections

    assert len(a.connections) == 2
    assert len(b.connections) == 2
    assert len(c.connections) == 2


def test_connect_port_to_two_other_ports_with_single_connection(a, b, c):
    a_single = Port(port_type=int, allows_multiple_connections=False)
    b_single = Port(port_type=int, allows_multiple_connections=False)
    c_single = Port(port_type=int, allows_multiple_connections=False)

    a_single.connect_to(b_single)

    assert a_single in b_single.connections
    assert b_single in a_single.connections

    a_single.connect_to(c_single)

    assert a_single not in b_single.connections
    assert b_single not in a_single.connections
    assert a_single in c_single.connections
    assert c_single in a_single.connections


def test_connect_port_to_self(a):
    with pytest.raises(ValueError):
        a.connect_to(a)


def test_connect_port_to_incompatible():
    p1 = Port(port_type=int)
    p2 = Port(port_type=str)

    with pytest.raises(ValueError):
        p1.connect_to(p2)


def test_disconnect_port_from_other(a, b):
    a.connect_to(b)

    b.disconnect_from(a)

    assert a not in b.connections
    assert b not in a.connections

    assert len(a.connections) == 0
    assert len(b.connections) == 0


def test_disconnect_port_twice(a, b):
    a.connect_to(b)

    b.disconnect_from(a)
    a.disconnect_from(b)

    assert a not in b.connections
    assert b not in a.connections

    assert len(a.connections) == 0
    assert len(b.connections) == 0


def test_clear_port_connections(a, b, c):
    a.connect_to(b)
    a.connect_to(c)

    a.clear_all_connections()

    assert len(a.connections) == 0
    assert a not in b.connections
    assert a not in c.connections
