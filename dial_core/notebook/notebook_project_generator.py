# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import dependency_injector.providers as providers
import nbformat as nbf
from dial_core.project import Project
from dial_core.node_editor import Scene
from dial_core.utils import log

from .node_transformers_registry import (
    NodeTransformersRegistry,
    NodeTransformersRegistrySingleton,
)

LOGGER = log.get_logger(__name__)


class NotebookProjectGenerator:
    def __init__(
        self, project: "Project", node_transformers_registry: "NodeTransformersRegistry"
    ):
        self._nodes_transformers_registry = node_transformers_registry

        self._project = project
        self._notebook = nbf.v4.new_notebook()

        self._generate_cells_from_scene(self._project.scene)

    @property
    def notebook(self):
        """Returns the Notebook object that represents the notebook."""
        return self._notebook

    def save_notebook_as(self, file_path: str):
        """Saves the notebook as a .ipynb file."""
        with open(file_path, "w") as notebook_file:
            nbf.write(self._notebook, notebook_file)

    def _generate_cells_from_scene(self, scene: "Scene"):
        cells = []
        for node in scene:
            try:
                cells += self._nodes_transformers_registry[node].transform(node)
            except KeyError:
                LOGGER.warn(f"{node} doesn't have any registered NodeTransformer.")

        self._notebook["cells"] = cells


NotebookProjectGeneratorFactory = providers.Factory(
    NotebookProjectGenerator,
    node_transformers_registry=NodeTransformersRegistrySingleton,
)
