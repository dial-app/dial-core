# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


from copy import deepcopy

from dial.utils import log

from .project import Project

LOGGER = log.get_logger(__name__)


class ProjectManager:
    def __init__(self, default_project: Project):
        super().__init__()

        # Project used as a base for new projects
        self.__default_project = default_project

        # Currently active projects
        self.__projects = [deepcopy(self.__default_project)]

        self.__active = self.__projects[0]

    @property
    def active(self):
        return self.__active

    def set_active_project(self, index):
        try:
            self.__active = self.__projects[index]

            LOGGER.info(
                "Active project changed: %s(%s)", index, self.__active,
            )

        except IndexError:
            pass

    def __len__(self):
        return len(self.__projects)

    def new_project(self):
        new_project = deepcopy(self.__default_project)

        self.__projects.append(new_project)

        # Activate the currently created project
        self.set_active_project(self.__projects.index(new_project))

        LOGGER.info("New project created")

    def open_project(self, file_path):
        LOGGER.info("Opening a new project... %s", file_path)

    def save_project(self):
        LOGGER.info("Saving currently active project...")

    def save_project_as(self, file_path):
        LOGGER.info("Saving currently active project as... %s", file_path)
