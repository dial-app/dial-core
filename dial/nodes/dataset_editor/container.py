# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .dataset_editor_node import DatasetEditorNode
from .dataset_editor_widget import DatasetEditorWidget
from .dataset_table import TrainTestTabsFactory

DatasetEditorWidgetFactory = providers.Factory(
    DatasetEditorWidget, train_test_tabs=TrainTestTabsFactory
)

DatasetEditorNodeFactory = providers.Factory(
    DatasetEditorNode, dataset_editor_widget=DatasetEditorWidgetFactory
)
