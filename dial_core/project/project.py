# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.node_editor import Scene


class Project:
    def __init__(self, name: str, scene: "Scene"):
        self.name = name
        self.file_path = ""

        self.__scene = scene

    @property
    def scene(self):
        """Returns the nodes scene of the project."""
        return self.__scene
