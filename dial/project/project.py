# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import DatasetLoader


class Project:
    """
    Dial project file.
    """

    def __init__(self):
        self.dataset_name = "Empty Dataset"
        self.dataset_brief = "..."
        self.train_dataset = None
        self.test_dataset = None
        self.dataset_x_type = None
        self.dataset_y_type = None

    def load_dataset(self, dataset_loader: DatasetLoader):
        self.dataset_name = dataset_loader.name
        self.dataset_brief = dataset_loader.brief

        train, test = dataset_loader.load()

        self.train_dataset = train
        self.test_dataset = test
        self.dataset_x_type = dataset_loader.x_type
        self.dataset_y_type = dataset_loader.y_type
