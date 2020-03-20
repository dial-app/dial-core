# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# import os
from typing import Optional

import dependency_injector.providers as providers

from dial_core.plugin import Plugin
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class PluginManager:
    def __init__(self, installed_plugins_dict=None):
        self.__installed_plugins = {}

        if installed_plugins_dict:
            self.__populate_installed_plugins(installed_plugins_dict)

    @property
    def installed_plugins(self):
        return self.__installed_plugins

    # def install_plugin(self, plugin_path: str) -> "Plugin":
    #     if not os.path.exists(plugin_path):
    #         raise FileNotFoundError(
    #             f"Can't import the plugin. Invalid path: {plugin_path}"
    #         )

    #     plugin = Plugin(plugin_path)
    #     self.__installed_plugins[plugin.name] = plugin

    #     return plugin

    def load_plugin(self, plugin_name: str) -> Optional["Plugin"]:
        plugin = self.__get_plugin_by_name(plugin_name)
        plugin.load()

        return plugin

    def unload_plugin(self, plugin_name: str):
        plugin = self.__get_plugin_by_name(plugin_name)
        plugin.unload()

    def __get_plugin_by_name(self, plugin_name):
        try:
            return self.__installed_plugins[plugin_name]

        except KeyError as err:
            LOGGER.warning("Can't load a plugin called %s", plugin_name)
            raise err

    def __populate_installed_plugins(self, installed_plugins_dict):
        for plugin_name in installed_plugins_dict:
            plugin = Plugin(plugin_name, installed_plugins_dict[plugin_name])
            self.__installed_plugins[plugin_name] = plugin

    def to_dict(self):
        return {
            key: value.to_dict() for (key, value) in self.__installed_plugins.items()
        }


PluginManagerSingleton = providers.Singleton(PluginManager)
