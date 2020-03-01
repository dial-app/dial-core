# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from dial_core.node_editor import Scene


class Project:
    def __init__(self, scene: "Scene" = Scene()):
        self.__scene = scene
