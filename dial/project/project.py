# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import Dataset, DatasetLoader


class Project:
    """
    Dial project file.
    """

    def __init__(
        self, default_dataset_info, default_model_info, default_parameters_info
    ):
        self.name = "Empty project"
        self.file_path = ""
        self.dataset = default_dataset_info
        self.model = default_model_info
        self.parameters = default_parameters_info


class DatasetInfo:
    def __init__(self):
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
        self.name = "Empty model"
        # self.model = None
        self.layers = []
        self.compiled = False

    def load_model(self, model_loader):
        self.name = model_loader.name
        # self.model = model_loader.load()
        self.layers = []
        self.compiled = True


class ParametersInfo:
    def __init__(self):
        self.loss = "binary_crossentropy"
        self.optimizer = "adam"

        self.epochs = 1

        self.metrics = ["accuracy"]

    def change_parameter(self, key, value):
        # Check if the attribute called "key" exists. Raise AttributeError if not found
        getattr(self, key, value)

        # If attribute was found, set a new value
        setattr(self, key, value)
