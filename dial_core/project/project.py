# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os

import dependency_injector.providers as providers

from dial_core.node_editor import Scene, SceneFactory


class Project:
    def __init__(self, name: str, scene: "Scene"):
        self.name = name
        self.file_path = ""

        self._scene = scene
        self._scene.parent = self

    @property
    def scene(self):
        """Returns the nodes scene of the project."""
        return self._scene

    def directory(self) -> str:
        """Returns the directory where the project's .dial file is."""
        return os.path.dirname(self.file_path)


DefaultProjectFactory = providers.Factory(
    Project, name="Default Project", scene=SceneFactory
)
