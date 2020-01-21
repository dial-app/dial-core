# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Graphic widgets that can be reused on the project. """

from .dataset_table import TrainTestTabs
from .datasets_list import DatasetsListDialog, PredefinedDatasetsListDialog
from .log import LoggerDialog, LoggerTextboxWidget
from .windows import Windows

__all__ = [
    "TrainTestTabs",
    "DatasetsListDialog",
    "PredefinedDatasetsListDialog",
    "LoggerDialog",
    "LoggerTextboxWidget",
    "Windows",
]
