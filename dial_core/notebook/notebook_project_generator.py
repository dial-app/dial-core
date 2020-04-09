# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import nbformat as nbf
from dial_core.project import Project, Scene


class NotebookProjectGenerator:
    def __init__(self, project: "Project"):
        self._project = project

        self._notebook = nbf.v4.new_notebook()

    def save_notebook_as(self, file_path: str):
        with open(file_path, "w") as notebook_file:
            nbf.write(self._notebook, notebook_file)

    def _generate_cells_from_scene(self, scene: "Scene"):
        cells = []
        for node in scene:
            cells += self.__nodes
