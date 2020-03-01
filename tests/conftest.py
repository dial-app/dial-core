import pytest

from dial_core import __version__
from dial_core.node_editor import InputPort, Node, OutputPort, Port

collect_ignore = ["setup.py"]


@pytest.fixture
def a_multi():
    """Empty port a. Allows multiple connections to different ports. """
    return Port(name="a_multi", port_type=int)


@pytest.fixture
def b_multi():
    """Empty port b. Allows multiple connections to different ports. """
    return Port(name="b_multi", port_type=int)


@pytest.fixture
def c_multi():
    """Empty port c. Allows multiple connections to different ports. """
    return Port(name="c_multi", port_type=int)


@pytest.fixture
def a_single():
    """Empty port a. Doesn't allow singleple connections to different ports. """
    return Port(name="a_single", port_type=int, allows_multiple_connections=False)


@pytest.fixture
def b_single():
    """Empty port b. Doesn't allow singleple connections to different ports. """
    return Port(name="b_single", port_type=int, allows_multiple_connections=False)


@pytest.fixture
def c_single():
    """Empty port c. Doesn't allows multiple connections to different ports. """
    return Port(name="c_multi", port_type=int, allows_multiple_connections=False)


@pytest.fixture
def port_int_a():
    return Port(name="port_int_a", port_type=int)


@pytest.fixture
def port_int_b():
    return Port(name="port_int_b", port_type=int)


@pytest.fixture
def port_str():
    return Port(name="port_str", port_type=str)


@pytest.fixture
def node_a():
    """Empty node a. Allows multiple connections to different ports. """
    return Node(title="a")


@pytest.fixture
def node_b():
    """Empty node b. Allows multiple connections to different ports. """
    return Node(title="b")


@pytest.fixture
def input_port_a():
    """Simple input port"""
    return InputPort(name="a", port_type=int)


@pytest.fixture
def output_port_a():
    """Simple input port"""
    return OutputPort(name="a", port_type=int)


def pytest_report_header(config):
    return f"Dial {__version__}"
