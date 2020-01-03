# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widgets for displaying a dialog with predefined datasets that can be loaded.
"""

import dependency_injector.providers as providers
from dial.datasets import PREDEFINED_DATASETS

from . import dialog, model, view

DatasetsListModel = providers.Factory(model.DatasetsListModel)

PredefinedDatasetsListModel = providers.Factory(
    model.DatasetsListModel, datasets_list=list(PREDEFINED_DATASETS.values())
)

DatasetsListView = providers.Factory(view.DatasetsListView)

DatasetsListDialog = providers.Factory(
    dialog.DatasetsListDialog, model=DatasetsListModel, view=DatasetsListView,
)

PredefinedDatasetsListDialog = providers.Factory(
    DatasetsListDialog, model=PredefinedDatasetsListModel
)

__all__ = ["DatasetsListDialog", "PredefinedDatasetsListModel"]
