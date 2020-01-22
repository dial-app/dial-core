# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Graphic widgets that can be reused on the project. """

from .dataset_table import TrainTestTabs
from .datasets_list import DatasetsList, PredefinedDatasetsList
from .log import Logger
from .menubars import MenuBars
from .model_table import ModelTable

__all__ = [
    "TrainTestTabs",
    "DatasetsList",
    "PredefinedDatasetsList",
    "Logger",
    "MenuBars",
    "ModelTable",
]
