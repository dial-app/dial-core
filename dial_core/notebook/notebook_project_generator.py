# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from collections import OrderedDict
from typing import Dict

import dependency_injector.providers as providers
import nbformat as nbf
from dial_core.node_editor import Scene
from dial_core.project import Project
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
        self._project = project
        self._notebook = nbf.v4.new_notebook()

        self._node_transformers = OrderedDict()
        self._nodes_transformers_registry = node_transformers_registry

        self._generate_transformers_for_scene(self._project.scene)
        self._generate_notebook()

    @property
    def notebook(self):
        """Returns the Notebook object that represents the notebook."""
        return self._notebook

    def save_notebook_as(self, file_path: str):
        """Saves the notebook as a .ipynb file."""
        with open(file_path, "w") as notebook_file:
            nbf.write(self._notebook, notebook_file)

    def _generate_transformers_for_scene(self, scene: "Scene"):
        for node in scene:
            try:
                self._node_transformers[
                    node
                ] = self._nodes_transformers_registry.create_transformer_from(node)
            except KeyError:
                LOGGER.warn(f"{node} doesn't have any registered NodeTransformer.")

    def _topological_sort(self, node_transformers: Dict["Node", "NodeTransformer"]):
        def recursive_sort(transformer, visited: set, sorted_transformers):
            visited.add(transformer)

            for neighbour in transformer.node.connected_output_nodes():
                neighbour_transformer = self._node_transformers[neighbour]

                if neighbour_transformer not in visited:
                    recursive_sort(neighbour_transformer, visited, sorted_transformers)

            sorted_transformers.append(transformer)

        sorted_transformers = []
        visited = set()

        for transformer in reversed(node_transformers.values()):
            if transformer not in visited:
                recursive_sort(transformer, visited, sorted_transformers)

        sorted_transformers.reverse()

        return sorted_transformers

    def _generate_notebook(self):
        cells = []
        for node_transformer in self._topological_sort(self._node_transformers):
            cells += node_transformer.cells()

        self._notebook["cells"] = cells

        return self._notebook


NotebookProjectGeneratorFactory = providers.Factory(
    NotebookProjectGenerator,
    node_transformers_registry=NodeTransformersRegistrySingleton,
)
