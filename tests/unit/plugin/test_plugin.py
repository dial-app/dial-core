# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import patch


def test_plugin_creation(plugin):
    assert plugin.name == "test-plugin"
    assert plugin.version == "0.1.2"
    assert plugin.summary == "A Test Plugin."
    assert plugin.active is True


def test_plugin_activate(plugin):
    with patch.object(plugin, "load") as plugin_load, patch.object(
        plugin, "unload"
    ) as plugin_unload:
        plugin.active = True
        plugin_load.assert_called()

        plugin.active = False
        plugin_unload.assert_called()


def test_plugin_load(plugin, test_plugin_package):
    plugin.load()

    assert plugin.active is True
    assert plugin.module is not None

    plugin.module.load_plugin.assert_called()

    # Version and summary are updated after importing
    assert plugin.version == test_plugin_package.version()
    assert plugin.summary == test_plugin_package.summary()


def test_plugin_unload(plugin):
    plugin.unload()

    assert plugin.active is False
    assert plugin.module is None


def test_plugin_to_dict(plugin):
    dictionary = plugin.to_dict()
    assert dictionary["version"] == plugin.version
    assert dictionary["summary"] == plugin.summary
    assert dictionary["active"] == plugin.active
