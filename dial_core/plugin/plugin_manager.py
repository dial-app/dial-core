# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# import os
from typing import Optional

import dependency_injector.providers as providers

from dial_core.plugin import Plugin
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class PluginManager:
    def __init__(self, installed_plugins_dict=None):
        self._installed_plugins = {}

        if installed_plugins_dict:
            self._populate_installed_plugins(installed_plugins_dict)

    @property
    def installed_plugins(self):
        return self._installed_plugins

    def load_plugin(self, plugin_name: str) -> Optional["Plugin"]:
        plugin = self._get_plugin_by_name(plugin_name)
        plugin.load()

        return plugin

    def unload_plugin(self, plugin_name: str):
        plugin = self._get_plugin_by_name(plugin_name)
        plugin.unload()

    def _get_plugin_by_name(self, plugin_name):
        try:
            return self._installed_plugins[plugin_name]

        except KeyError as err:
            LOGGER.warning("Can't load a plugin called %s", plugin_name)
            raise err

    def _populate_installed_plugins(self, installed_plugins_dict):
        for plugin_name in installed_plugins_dict:
            plugin = Plugin(plugin_name, installed_plugins_dict[plugin_name])
            self._installed_plugins[plugin_name] = plugin

    def to_dict(self):
        return {
            key: value.to_dict() for (key, value) in self._installed_plugins.items()
        }


PluginManagerSingleton = providers.Singleton(PluginManager)
