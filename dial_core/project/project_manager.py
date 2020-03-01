# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle
from copy import deepcopy
from typing import TYPE_CHECKING

from dial_core.utils import Timer, log

if TYPE_CHECKING:
    from .project import Project

LOGGER = log.get_logger(__name__)


class ProjectManager:
    def __init__(self, default_project: "Project"):
        self.__default_project = default_project

        self.__projects = [deepcopy(self.__default_project)]

        self.__active = self.__projects[0]

    @property
    def active(self):
        return self.__active

    def set_active_project(self, index: int):
        try:
            self.__active = self.__projects[index]

            LOGGER.info(
                "Active project changed: %s(%s)", index, self.__active,
            )

        except IndexError:
            pass

    def new_project(self, new_project: "Project" = None):
        if not new_project:
            new_project = deepcopy(self.__default_project)

        self.__projects.append(new_project)

        self.set_active_project(self.__projects.index(new_project))

    def open_project(self, file_path: str):
        LOGGER.info("Opening a new project... %s", file_path)

        with open(file_path, "rb") as project_file:
            LOGGER.info("Loading project...")
            with Timer() as timer:
                project_in = pickle.load(project_file)

                self.new_project(project_in)

            LOGGER.info("Project loaded in %s ms", timer.elapsed())

            project_in.file_path = file_path
            LOGGER.info("New project file path is %s", file_path)

    def save_project(self):
        if not self.__active.file_path:
            raise ValueError("Project doesn't has a file_path set!")

        with open(self.active.file_path, "wb") as project_file:
            LOGGER.info("Saving project: %s", self.__active.file_path)

            with Timer() as timer:
                pickle.dump(self.__active, project_file)

            LOGGER.info("Project saved in %s ms", timer.elapsed())

    def save_project_as(self, file_path: str):
        self.active.file_path = file_path
        LOGGER.info("New file path for the project: %s", file_path)

        self.save_project()
