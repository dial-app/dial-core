# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import threading
from enum import Enum

from tensorflow.keras.layers import Input
from tensorflow.keras.models import Sequential

from dial.datasets import Dataset, DatasetLoader
from dial.utils import log

LOGGER = log.get_logger(__name__)


training_thread = None


class Project:
    """
    Dial project file.
    """

    class TrainingStatus(Enum):
        Running = 1
        Stopped = 2

    def __init__(
        self, default_dataset_info, default_model_info, default_parameters_info
    ):
        self.name = "Empty project"
        self.file_path = ""
        self.dataset = default_dataset_info
        self.model = default_model_info
        self.parameters = default_parameters_info

        self.training_status = self.TrainingStatus.Stopped
        # self.training_thread = threading.Thread(target=self.__train_model_async)

    def compile_model(self):
        self.model.model = Sequential()

        input_shape = self.dataset.train.input_shape

        LOGGER.info("Input shape %s", input_shape)
        LOGGER.info("Batch size: %s", self.dataset.train.batch_size)

        # Add an Input layer first
        self.model.model.add(Input(input_shape))

        # Add the rest of the layers
        [self.model.model.add(layer) for layer in self.model.layers]

        self.model.model.summary(print_fn=LOGGER.info)

        self.model.model.compile(
            optimizer=self.parameters.optimizer,
            loss=self.parameters.loss_function,
            metrics=["accuracy"],
        )

        LOGGER.info("Model compiled!")
        self.model.compiled = True

    def start_training_model_async(self):
        LOGGER.info("Start training the model...")

        global training_thread

        if self.training_status == self.TrainingStatus.Stopped:
            training_thread = threading.Thread(target=self.__train_model_async)
            training_thread.start()

            self.TrainingStatus = self.TrainingStatus.Running

    def stop_training_model(self):
        LOGGER.info("Training stopped...l")

        self.TrainingStatus = self.TrainingStatus.Stopped

    def __train_model_async(self):
        self.model.model.fit(
            self.dataset.train, epochs=self.parameters.epochs,
        )

        self.TrainingStatus = self.TrainingStatus.Stopped


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
        self.model = Sequential()
        self.layers = []
        self.compiled = False

    def load_model(self, model_loader):
        self.name = model_loader.name
        self.model = model_loader.load()
        self.layers = self.model.layers
        self.compiled = True


class ParametersInfo:
    def __init__(self):
        self.loss_function = "binary_crossentropy"
        self.optimizer = "adam"

        self.epochs = 1

        self.metrics = ["accuracy"]

    def change_parameter(self, key, value):
        # Check if the attribute called "key" exists. Raise AttributeError if not found
        getattr(self, key, value)

        # If attribute was found, set a new value
        setattr(self, key, value)

        self.compiled = False
