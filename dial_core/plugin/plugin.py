# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import importlib

import pkg_resources

from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class Plugin:
    def __init__(self, name: str, plugins_specs: dict):
        self._name = name
        self._version = plugins_specs["version"]
        self._summary = plugins_specs["summary"]
        self._active = plugins_specs["active"]

        self._module = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def summary(self) -> str:
        return self._summary

    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, toggle: bool):
        self._active = toggle

        if self._active:
            self.load()
        else:
            self.unload()

    @property
    def module(self):
        return self._module

    def load(self):
        module_importable_name = self.name.replace("-", "_")
        self._module = importlib.import_module(module_importable_name)

        try:
            self._module.load_plugin()
            self._update_plugin_metadata()
        except AttributeError as err:  # pragma: no cover
            LOGGER.warning("Error with `load_plugin` for %s.", self.name)
            LOGGER.exception(err)

        self._active = True

    def unload(self):
        try:
            self._module.unload_plugin()
        except AttributeError as err:  # pragma: no cover
            LOGGER.warning("Error with `unload_plugin` for %s.", self.name)
            LOGGER.exception(err)

        self._active = False
        self._module = None

    def _update_plugin_metadata(self):
        try:

            def get_metadata_value(key: str, package):
                for line in package.get_metadata_lines("PKG-INFO"):
                    (k, v) = line.split(": ", 1)
                    if k == key:
                        return v

            package = pkg_resources.require(self.name)[0]
            self._version = get_metadata_value("Version", package)
            self._summary = get_metadata_value("Summary", package)
        except FileNotFoundError as err:  # pragma: no cover
            LOGGER.exception(err)

    def to_dict(self):
        return {"version": self.version, "summary": self.summary, "active": self.active}
