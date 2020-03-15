# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import sys
import os
import importlib

import dependency_injector.providers as providers


class PluginManager:
    def __init__(self):
        pass

    def load_plugin(self, module_path):
        sys.path.append(module_path)

        module_name = os.path.basename(os.path.normpath(module_path))
        module = importlib.import_module(module_name)
        # obj = importlib.import_module(f"{module.__package__}.test_node.TestNode")
        # print(obj)

        return module

    def unload_plugin(self, module_path):
        pass


PluginManagerSingleton = providers.Singleton(PluginManager)
