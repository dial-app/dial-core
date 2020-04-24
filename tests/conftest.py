# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import Mock, patch

import pytest

from dial_core.node_editor import InputPort, Node, NodeRegistry, OutputPort, Port, Scene
from dial_core.notebook import NodeCellsRegistryFactory, NotebookProjectGeneratorFactory
from dial_core.plugin import Plugin, PluginManager
from dial_core.project import Project, ProjectManager

collect_ignore = ["setup.py"]

INSTALLED_PLUGINS = {
    "test-plugin": {"version": "0.1.2", "summary": "A Test Plugin.", "active": True}
}


def print_value(value):
    print(value)


def return_value():
    return 10


@pytest.fixture
def test_plugin_package():
    test_plugin_mock = Mock()
    test_plugin_mock.get_metadata_lines.return_value = [
        "Version: 0.3.4",
        "Summary: Test Plugin",
    ]
    test_plugin_mock.version.return_value = "0.3.4"
    test_plugin_mock.summary.return_value = "Test Plugin"

    return test_plugin_mock


@pytest.fixture
def plugin(test_plugin_package):
    plugin_specs = INSTALLED_PLUGINS["test-plugin"]

    module_mock = Mock()
    module_mock.load_plugin.return_value = True
    module_mock.unload_plugin.return_value = True

    with patch("importlib.import_module") as import_mock, patch(
        "pkg_resources.require"
    ) as require_mock:
        import_mock.return_value = module_mock
        require_mock.return_value = [test_plugin_package]

        yield Plugin("test-plugin", plugin_specs)


@pytest.fixture
def plugin_manager(plugin):
    with patch("dial_core.plugin.plugin_manager.Plugin", return_value=plugin), patch(
        "os.path.exists", return_value=True
    ):
        plugin_manager = PluginManager(installed_plugins_dict=INSTALLED_PLUGINS)

    return plugin_manager


@pytest.fixture
def scene():
    """Returns an empty, default scene."""
    return Scene()


@pytest.fixture
def node_registry():
    """Returns an empty NodeRegistry object."""
    return NodeRegistry()


@pytest.fixture
def project_a(scene):
    """Returns a default (empty) project."""
    return Project(name="ProjectA", scene=scene)


@pytest.fixture
def project_manager_default_scene():
    """Returns an empty, default scene."""
    return Scene()


@pytest.fixture
def project_manager_default_project(project_manager_default_scene):
    """Returns a project used by default by the ProjectManager instances."""
    return Project(name="TestProject", scene=project_manager_default_scene)


@pytest.fixture
def project_manager(project_manager_default_project):
    """Returns a ProjectManager object."""
    return ProjectManager(default_project=project_manager_default_project)


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
def input_port_b():
    """Simple input port"""
    return InputPort(name="b", port_type=int)


@pytest.fixture
def output_port_a():
    """Simple input port"""
    return OutputPort(name="a", port_type=int)


@pytest.fixture
def output_port_b():
    """Simple input port"""
    return OutputPort(name="b", port_type=int)


@pytest.fixture
def notebook_project_generator(project_a):
    return NotebookProjectGeneratorFactory()


@pytest.fixture
def node_transformers_registry():
    return NodeCellsRegistryFactory()
