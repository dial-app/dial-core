# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

try:
    import cPickle as pickle
except ImportError:
    import pickle  # type: ignore

from copy import deepcopy

from dial.utils import Timer, log

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

    def load_dataset(self, dataset_loader):
        self.active.dataset.load_dataset(dataset_loader)

    def load_model(self, model_loader):
        self.active.model.load_model(model_loader)

    def change_parameter(self, key, value):
        if key == "batch_size":  # TODO: CHANGE
            self.active.dataset.train.batch_size = value
            self.active.dataset.test.batch_size = value

        self.active.parameters.change_parameter(key, value)
        LOGGER.info("New %s value: %s", key, value)

    def compile_model(self):
        self.active.compile_model()

    def train_model(self):
        self.active.train_model()

    def new_project(self, new_project=None):
        self.__add_new_project(new_project)

        LOGGER.info("New project created!")

    def open_project(self, file_path):
        LOGGER.info("Opening a new project... %s", file_path)

        with open(file_path, "rb") as project_file:
            LOGGER.info("Loading project...")
            with Timer() as timer:
                project_in = pickle.load(project_file)

                self.__add_new_project(project_in)

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

    def save_project_as(self, file_path):
        self.active.file_path = file_path
        LOGGER.info("New file path for the project: %s", file_path)

        self.save_project()

    def __add_new_project(self, new_project=None):
        if not new_project:  # Add a new default project
            new_project = deepcopy(self.__default_project)

        self.__projects.append(new_project)

        # Activate the currently created project
        self.set_active_project(self.__projects.index(new_project))
