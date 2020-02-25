# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.base.datasets import PredefinedDatasetLoaders

from . import dialog, model, view


class DatasetsList(containers.DeclarativeContainer):
    """
    Container for creating widgets with a list of datasets.
    """

    Model = providers.Factory(model.DatasetsListModel)
    View = providers.Factory(view.DatasetsListView)

    Dialog = providers.Factory(dialog.DatasetsListDialog, model=Model, view=View,)


class PredefinedDatasetsList(containers.DeclarativeContainer):
    """
    Container for creating a list with a list of predefined datasets.
    """

    Model = providers.Factory(
        model.DatasetsListModel,
        datasets_list=[
            loader() for loader in PredefinedDatasetLoaders.providers.values()
        ],
    )

    Dialog = providers.Factory(DatasetsList.Dialog, model=Model)
