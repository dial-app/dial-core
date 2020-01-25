# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Classes for loading models.
"""

from abc import ABCMeta, abstractmethod
from typing import List, Tuple

from dial.datasets import Dataset, datatype
from dial.utils import Timer, log
from tensorflow.keras.applications import vgg16

LOGGER = log.get_logger(__name__)


class ModelLoader(metaclass=ABCMeta):
    def __init__(self, name: str, brief: str):
        self.name = name
        self.brief = brief

    def load(self):
        with Timer() as timer:
            model = self._load_data()

        LOGGER.info("Fetched model data in %s ms", timer.elapsed())

        return model

    @abstractmethod
    def _load_data(self):
        """
        Return the train/test pairs.
        """

    def __str__(self) -> str:
        return self.name


class VGG16Loader(ModelLoader):
    """
    VGG16 model loader.
    """

    def __init__(self):
        super().__init__("VGG16", "Convolutional neural network")

    def _load_data(self):
        return vgg16.VGG16()
