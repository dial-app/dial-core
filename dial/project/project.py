# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import Dataset, DatasetLoader


class Project:
    """
    Dial project file.
    """

    def __init__(self, default_dataset_info, default_model_info):
        super().__init__()

        self.name = "Empty project"
        self.file_path = ""
        self.dataset = default_dataset_info
        self.model = default_model_info


class DatasetInfo:
    def __init__(self):
        super().__init__()

        self.name = "Empty Dataset"
        self.brief = "..."
        self.train = Dataset()
        self.test = Dataset()
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


class ModelInfo:
    def __init__(self):
        super().__init__()

        self.name = "Empty model"
        # self.model = None
        self.layers = []
        self.compiled = False

    def load_model(self, model_loader):
        pass
        # self.name = model_loader.name
        # self.model = model_loader.load()
        # self.layers = self.model.layers
        # self.compiled = True

        # self.model_changed.emit()
