# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# pylint: disable=C0103

"""
Widgets for displaying a dialog with predefined datasets that can be loaded.
"""

import dependency_injector.providers as providers

from dial.datasets import PREDEFINED_DATASETS

from . import dialog, model, view

# List of datasets
DatasetsListModel = providers.Factory(model.DatasetsListModel)

DatasetsListView = providers.Factory(view.DatasetsListView)

DatasetsListDialog = providers.Factory(
    dialog.DatasetsListDialog, model=DatasetsListModel, view=DatasetsListView,
)

PredefinedDatasetsListModel = providers.Factory(
    model.DatasetsListModel, datasets_list=list(PREDEFINED_DATASETS.values())
)


PredefinedDatasetsListDialog = providers.Factory(
    DatasetsListDialog, model=PredefinedDatasetsListModel
)

__all__ = ["DatasetsListDialog", "PredefinedDatasetsListModel"]
