# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial.datasets import DatasetLoader


class Project:
    """
    Dial project file.
    """

    class DatasetInfo:
        def __init__(self):
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

    def __init__(self):
        self.dataset = self.DatasetInfo()
