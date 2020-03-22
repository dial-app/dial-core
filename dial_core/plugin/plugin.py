# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import importlib

import pkg_resources

from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class Plugin:
    def __init__(self, name: str, plugins_specs: dict):
        self.__name = name
        self.__version = plugins_specs["version"]
        self.__summary = plugins_specs["summary"]
        self.__active = plugins_specs["active"]

        self.__module = None

    @property
    def name(self) -> str:
        return self.__name

    @property
    def version(self) -> str:
        return self.__version

    @property
    def summary(self) -> str:
        return self.__summary

    @property
    def active(self) -> bool:
        return self.__active

    @active.setter
    def active(self, toggle: bool):
        self.__active = toggle

        if self.__active:
            self.load()
        else:
            self.unload()

    @property
    def module(self):
        return self.__module

    def load(self):
        module_importable_name = self.name.replace("-", "_")
        self.__module = importlib.import_module(module_importable_name)

        try:
            self.__module.load_plugin()
            self.__update_plugin_metadata()
        except AttributeError:  # pragma: no cover
            LOGGER.warning("No `load_plugin` method found for %s.", self.name)

        self.__active = True

    def unload(self):
        try:
            self.__module.unload_plugin()
        except AttributeError:  # pragma: no cover
            LOGGER.warning("No `unload_plugin` method found for %s.", self.name)

        self.__active = False
        self.__module = None

    def __update_plugin_metadata(self):
        try:

            def get_metadata_value(key: str, package):
                for line in package.get_metadata_lines("PKG-INFO"):
                    (k, v) = line.split(": ", 1)
                    if k == key:
                        return v

            package = pkg_resources.require(self.name)[0]
            self.__version = get_metadata_value("Version", package)
            self.__summary = get_metadata_value("Summary", package)
        except FileNotFoundError as err:  # pragma: no cover
            LOGGER.exception(err)

    def to_dict(self):
        return {"version": self.version, "summary": self.summary, "active": self.active}
