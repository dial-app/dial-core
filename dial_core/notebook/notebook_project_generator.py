# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from collections import OrderedDict
from typing import Dict, Optional, Set

import dependency_injector.providers as providers
import nbformat as nbf

from dial_core.node_editor import Node, Scene
from dial_core.project import Project
from dial_core.utils import log

from .node_cells import NodeCells
from .node_cells_registry import NodeCellsRegistry, NodeCellsRegistrySingleton

LOGGER = log.get_logger(__name__)


class NotebookProjectGenerator:
    """The NotebookProjectGenerator class provides a transformer from Projects to
    Notebooks.

    The class will take the project scene nodes, sort them in topological order and use
    a transformer for convert each node into a set of cells compatible with Jupyter
    Notebooks.
    """

    def __init__(
        self, node_cells_registry: "NodeCellsRegistry", project: "Project" = None,
    ):
        self._notebook = nbf.v4.new_notebook()

        self._project: Optional["Project"] = Project

        self._external_packages: Set[str] = set(["dial-core"])

        self._node_transformers = OrderedDict()
        self._nodes_transformers_registry = node_cells_registry

        self.set_project(project)

    @property
    def notebook(self):
        """Returns the Notebook object that represents the notebook."""
        return self._notebook

    def get_project(self) -> "Project":
        """Returns the project associated with this notebook."""
        return self._project

    def set_project(self, project):
        """Sets a new project for this generator.

        If a valid project is passed, generates the transformers and makes the instance
        ready for generating the notebook.
        """
        self.clear()

        self._project = project
        if self._project:
            self._add_transformers_from_scene(self._project.scene)

    def update_project_changes(self):
        """Updates the notebook to reflect changes on the project (like new or removed
        nodes)."""
        project = self._project

        self.clear()
        self.set_project(project)

    def save_notebook_as(self, file_path: str):
        """Saves the notebook as an .ipynb file."""
        with open(file_path, "w") as notebook_file:
            nbf.write(self._notebook, notebook_file)

    def clear(self):
        """Clears the project and registered transformers, and sets a new notebook."""
        self._notebook = nbf.v4.new_notebook()

        self._project = None
        self._node_transformers.clear()
        self._external_packages = set(["dial-core"])

    def _add_transformers_from_scene(self, scene: "Scene"):
        """Creates a new transformer for each node in the scene.

        If the node can't be converted to a transformer, a log message is displayed but
        no error is raised.
        """
        for node in scene:
            self._add_node_as_transformer(node)

        self._sort_topologically()
        self._generate_notebook()

    def _add_node_as_transformer(self, node: "Node"):
        """Tries to add the associated transformer for the node."""
        try:
            self._node_transformers[
                node
            ] = self._nodes_transformers_registry.create_transformer_from(node)
            self._detect_external_package(node)

        except KeyError:
            LOGGER.warn(f"{node} doesn't have any registered NodeTransformer.")

    def _generate_notebook(self):
        """Updates the notebook object, populating it with the cells generated by the
        transformers."""
        cells = [self._external_packages_cells()]
        for node_transformer in reversed(self._node_transformers.values()):
            cells += node_transformer.cells()

        self._notebook["cells"] = cells

        return self._notebook

    def _detect_external_package(self, node: "Node"):
        pass
        # TODO: Not working as intended
        # module_name = inspect.getmodule(node)
        # self._external_packages.add(module_name)

    def _external_packages_cells(self):
        install_cell_text = "# External packages"

        for external_package in self._external_packages:
            install_cell_text += f"\n%pip install {external_package}"

        return nbf.v4.new_code_cell(install_cell_text)

    def _sort_topologically(self):
        """Sorts the dictionary `self._node_transformers` in topologically order.

        This order ensures that variables representing the ports are defined before
        used. See "graph topological sort" for more information.

        This algorithm runs in O(n) time.
        """

        def recursive_topo_sort(
            transformer: "NodeCells",
            visited: set,
            sorted_transformers: Dict["Node", "NodeCells"],
        ):
            # Using a visited set is esential for not repeating nodes.
            visited.add(transformer)

            for neighbour in transformer.node.connected_output_nodes():
                neighbour_transformer = self._node_transformers[neighbour]

                if neighbour_transformer not in visited:
                    recursive_topo_sort(
                        neighbour_transformer, visited, sorted_transformers
                    )

            # After we've visited and inserted all childs, insert this transformer
            sorted_transformers[transformer.node] = transformer

        sorted_transformers = OrderedDict()
        visited = set()

        # 1. Running the algorithm through all transformers in a loop ensures that all
        # subgraphs are sorted.
        # 2. Running in reverse order normally gives a more "natural" ordering for nodes
        # that have the ranking.
        # For example, for a graph like:
        #       0 -> [1]
        #       1 -> []
        #       2 -> [3]
        #       3 -> []
        # The topological order is:
        # 2 3 0 1
        # But running on reverse will give:
        # 0 1 2 3
        # Both are valid topological orders, but we prefer using the second one as
        # elements preserve the insertion order.
        for transformer in reversed(self._node_transformers.values()):
            if transformer not in visited:
                recursive_topo_sort(transformer, visited, sorted_transformers)

        self._node_transformers = sorted_transformers


NotebookProjectGeneratorFactory = providers.Factory(
    NotebookProjectGenerator, node_cells_registry=NodeCellsRegistrySingleton,
)
