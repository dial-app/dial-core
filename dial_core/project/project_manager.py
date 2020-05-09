# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
import pickle
from copy import deepcopy
from typing import TYPE_CHECKING, List

import dependency_injector.providers as providers

from dial_core.utils import Timer, log

from .project import DefaultProjectFactory

if TYPE_CHECKING:
    from .project import Project

LOGGER = log.get_logger(__name__)


class ProjectManager:
    """
    The ProjectManager class provides an interface that acts as a container for Project
    objects, and also has the necessary tools to create and open projects from files in
    the system.

    Attributes:
        active: Currently active project.
    """

    def __init__(self, default_project: "Project"):
        self._default_project = default_project

        self._projects: List["Project"] = []
        self.new_project()

    @property
    def projects(self):
        return self._projects

    @property
    def active(self) -> "Project":
        """Returns the currently active project.

        The active project can be accessed directly by using this property.

        See `set_active_project` to learn how to change the active project.
        """
        return self._active

    def projects_count(self) -> int:
        """Returns the number of created projects."""
        return len(self._projects)

    def index_of(self, project: "Project") -> int:
        """Returns the index of the project, or -1 if not found."""
        try:
            return self._projects.index(project)
        except ValueError:
            return -1

    def new_project(self) -> "Project":
        """Adds a new default project to the project manager.

        A copy of a default project (The one defined on the variable
        `self._default_project` will be added)

        Returns:
            The recently added active project
        """
        new_project = self._new_project_impl()
        LOGGER.debug("New project created: %s", new_project)

        return self.add_project(new_project)

    def add_project(self, project: "Project") -> "Project":
        """Adds a project to the project manager and makes it the new active project.

        Returns:
            The recently added active project.
        """

        self._add_project_impl(project)
        LOGGER.debug("Project added to the projects list: %s", self._projects)

        # Activate last project
        return self.set_active_project(self.projects_count() - 1)

    def set_active_project(self, index: int) -> "Project":
        """Selects a project from the created ones and makes it the active project.

        Returns:
            The new active project.

        Raises:
            IndexError: If there isn't a project with index `index`.
        """
        self._set_active_project_impl(index)
        LOGGER.info(
            "Active project changed: %s(%s)", index, self._active,
        )

        return self._active

    def close_project(self, project: "Project"):
        index = self.projects.index(project)

        self._remove_project_impl(project)
        LOGGER.info("Closed project: %s", project)

        self.set_active_project(max(min(index, self.projects_count() - 1), 0))

    def open_project(self, file_path: str) -> "Project":
        """Opens a new project from a `.dial` file.

        Then, the project manager will automatically change its active project to the
        new opened one.

        Returns:
            The opened project (Which is the same as `project_manager.active`)

        Raises:
            FileNotFoundError: If the `file_path` is invalid.
        """
        LOGGER.info("Opening a new project... %s", file_path)

        with open(file_path, "rb") as project_file:
            LOGGER.info("Loading project...")
            with Timer() as timer:
                opened_project = pickle.load(project_file)

                self.add_project(opened_project)

            LOGGER.info("Project loaded in %s ms", timer.elapsed())

            opened_project.file_path = file_path
            LOGGER.info("New project file path is %s", file_path)

        return opened_project

    def save_project(self, project: "Project") -> "Project":
        """Saves the project on its defined file path.

        The project MUST have a file path. Otherwise, it will throw a ValueError
        exception.

        For saving a project specifying a new file path, see `save_project_as`.

        Raises:
            ValueError: If the project doesn't have a `file_path` defined.
        """
        if not project.file_path:
            raise ValueError("Project doesn't has a file_path set!")

        with open(project.file_path, "wb") as project_file:
            LOGGER.info("Saving project: %s", project.file_path)

            with Timer() as timer:
                pickle.dump(project, project_file)

            LOGGER.info("Project saved in %s ms", timer.elapsed())

        return project

    def save_project_as(self, project: "Project", parent_dir: str) -> "Project":
        """Save the project on a new file path.

        Once a project has been saved with `save_project_as`, it can also be saved with
        `save_project`, which will use the project's file path automatically.

        Important:
            The new `file_path` will be set as the project file path, replacing any
            previous paths.
        """
        project_dir = os.path.join(parent_dir, project.name)
        os.makedirs(project_dir, exist_ok=True)

        file_path = os.path.join(project_dir, f"{project.name}.dial")

        project.file_path = file_path
        LOGGER.info("New file path for the project: %s", file_path)

        return self.save_project(project)

    def _new_project_impl(self) -> "Project":
        return deepcopy(self._default_project)

    def _add_project_impl(self, project: "Project") -> "Project":
        self._projects.append(project)
        return project

    def _set_active_project_impl(self, index: int) -> "Project":
        self._active = self._projects[index]
        return self._active

    def _remove_project_impl(self, project: "Project") -> "Project":
        index = self._projects.index(project)
        del self._projects[index]

        if self.projects_count() == 0:
            self.new_project()

        return project


ProjectManagerFactory = providers.Factory(
    ProjectManager, default_project=DefaultProjectFactory
)

ProjectManagerSingleton = providers.Singleton(
    ProjectManager, default_project=DefaultProjectFactory
)
