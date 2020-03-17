# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import importlib
import os
import sys

import toml

from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class Plugin:
    def __init__(self, plugin_path: str):
        self.__path = plugin_path
        self.__pyproject = self._load_pyproject(self.__path)

        self.__module = None
        self.__active = False
        self.__loaded = False

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @property
    def description(self) -> str:
        return self.__description

    @property
    def path(self) -> str:
        return self.__path

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, toggle: bool):
        self.__active = toggle

    @property
    def loaded(self) -> bool:
        return self.__loaded

    def load(self):
        sys.path.append(self.__path)

        module_name = os.path.basename(os.path.normpath(self.__path)).replace("-", "_")
        self.__module = importlib.import_module(module_name)

        self.__loaded = True

        try:
            self.__module.initialize_plugin()
        except AttributeError:
            LOGGER.warning("No `initialize_plugin` method found for `module_name`.")

        self.__active = True

    def unload(self):
        # Remove from sys
        # Unload package (?)
        # Read something about using `del`
        self.__loaded = False
        self.__active = False

    def _load_pyproject(self, plugin_path: str):
        pyproject = toml.load(self.__path + "/pyproject.toml")

        self.__name = pyproject["tool"]["poetry"]["name"]
        self.__version = pyproject["tool"]["poetry"]["version"]
        self.__description = pyproject["tool"]["poetry"]["description"]
