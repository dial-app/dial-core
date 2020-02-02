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

    @active.setter
    def active(self, i):
        try:
            self.__active = self.__projects[i]

            LOGGER.debug(
                "Active project changed: %s (%s)",
                self.__projects.index(self.__active),
                self.__active,
            )

        except IndexError:
            pass

    def new_project(self):
        self.__projects.append(deepcopy(self.__default_project))

        # Activate the currently created project
        self.active = len(self.__projects) - 1

        LOGGER.info("New project created")

    def open_project(self, file_path):
        LOGGER.info("Opening a new project... %s", file_path)

    def save_project(self):
        LOGGER.info("Saving currently active project...")

    def save_project_as(self, file_path):
        LOGGER.info("Saving currently active project as... %s", file_path)
