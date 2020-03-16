# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import Mock, patch

import pytest
import toml

from dial_core.plugin import Plugin


@pytest.fixture
def plugin():
    TOML_FILE = """
    [tool.poetry]
    name = "test-plugin"
    version = "0.1.2"
    description = "A Test Plugin."
    """

    module_mock = Mock()

    with patch("dial_core.plugin.plugin.toml") as toml_mock, patch(
        "importlib.import_module"
    ) as import_mock:
        toml_mock.load.return_value = toml.loads(TOML_FILE)
        import_mock.return_value = module_mock

        yield Plugin("test-plugin")


def test_plugin_creation(plugin):
    assert plugin.name == "test-plugin"
    assert plugin.version == "0.1.2"
    assert plugin.description == "A Test Plugin."
    assert plugin.path == "test-plugin"
    assert not plugin.active
    assert not plugin.loaded


def test_plugin_load(plugin):
    plugin.load()

    assert plugin.loaded is True
    assert plugin.active is True
