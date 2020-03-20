# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest


def test_installed_plugins(plugin_manager):
    assert len(plugin_manager.installed_plugins) == 1

    assert plugin_manager.installed_plugins["test-plugin"] is not None


def test_load_plugin(plugin_manager):
    plugin_manager.load_plugin("test-plugin")
    assert plugin_manager.installed_plugins["test-plugin"].active is True


def test_load_inexistent_plugin(plugin_manager):
    with pytest.raises(KeyError):
        plugin_manager.load_plugin("inexistent-plugin")


def test_unload_plugin(plugin_manager):
    plugin_manager.unload_plugin("test-plugin")
    assert plugin_manager.installed_plugins["test-plugin"].active is False


def test_unload_inexistent_plugin(plugin_manager):
    with pytest.raises(KeyError):
        plugin_manager.unload_plugin("inexistent-plugin")


def test_plugin_manager_to_dict(plugin_manager, plugin):
    dictionary = plugin_manager.to_dict()
    assert "test-plugin" in dictionary
    assert dictionary["test-plugin"] == plugin.to_dict()
