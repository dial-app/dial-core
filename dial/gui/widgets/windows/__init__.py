# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# pylint: disable=C0103

"""
Window widgets displayed on the main window tabs.
"""
from . import datasets_window
from dial.gui.widgets import TrainTestTabs

import dependency_injector.providers as providers

DatasetsWindow = providers.Factory(
    datasets_window.DatasetsWindow, dataset_table_widget=TrainTestTabs()
)

__all__ = ["DatasetsWindow"]
