# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.models import PredefinedModelLoaders

from . import dialog, model, view


class ModelLoadersList(containers.DeclarativeContainer):
    """
    Container for creating widgets with a list of datasets.
    """

    Model = providers.Factory(model.ModelLoadersListModel)
    View = providers.Factory(view.ModelLoadersListView)

    Dialog = providers.Factory(dialog.ModelLoadersListDialog, model=Model, view=View,)


class PredefinedModelLoadersList(containers.DeclarativeContainer):
    """
    Container for creating a list with a list of predefined models.
    """

    Model = providers.Factory(
        model.ModelLoadersListModel,
        models_list=[loader() for loader in PredefinedModelLoaders.providers.values()],
    )

    Dialog = providers.Factory(ModelLoadersList.Dialog, model=Model)
