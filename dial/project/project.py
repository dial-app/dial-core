# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# try:
#     import cPickle as pickle
# except ImportError:
#     import pickle

from dial.datasets import DatasetLoader
from dial.utils import Timer, log
from PySide2.QtCore import QObject, Signal

LOGGER = log.get_logger(__name__)


class Project(QObject):
    """
    Dial project file.
    """

    dataset_changed = Signal(QObject)
    model_changed = Signal(QObject)

    def __init__(self):
        super().__init__()

        self.file_path = ""
        self.dataset = DatasetInfo()
        self.model = ModelInfo()

        self.dataset.dataset_changed.connect(lambda: self.dataset_changed.emit(self))
        self.model.model_changed.connect(lambda: self.model_changed.emit(self))

    def load(self, file_path):
        with open(file_path, "rb") as _:  # project_file:
            LOGGER.info("Loading project...")
            with Timer() as timer:
                pass
                # TODO: Load object from file

            LOGGER.info("Project loaded in %s ms", timer.elapsed())

            self.file_path = file_path
            LOGGER.info("New project file path is %s", self.file_path)

            self.project_changed.emit(self)

    def save_as(self, file_path):
        self.file_path = file_path
        self.save()

    def save(self):
        if not self.file_path:
            raise ValueError("File path for saving the project can't be empty.")

        with open(self.file_path, "wb") as _:  # project_file:
            LOGGER.info("Saving project...")
            with Timer() as timer:
                pass
                # TODO: Save object to file

            LOGGER.info("Project saved in %s ms", timer.elapsed())


class DatasetInfo(QObject):
    dataset_changed = Signal()

    def __init__(self):
        super().__init__()

        self.name = "Empty Dataset"
        self.brief = "..."
        self.train = None
        self.test = None
        self.x_type = None
        self.y_type = None

    def load_dataset(self, dataset_loader: DatasetLoader):
        self.name = dataset_loader.name
        self.brief = dataset_loader.brief

        train, test = dataset_loader.load()

        self.train = train
        self.test = test
        self.x_type = dataset_loader.x_type
        self.y_type = dataset_loader.y_type

        self.dataset_changed.emit()


class ModelInfo(QObject):
    model_changed = Signal()

    def __init__(self):
        super().__init__()

        self.name = "Empty model"
        self.model = None

    def load_model(self, model_loader):
        self.name = model_loader.name
        self.model = model_loader.load()

        self.model_changed.emit()
