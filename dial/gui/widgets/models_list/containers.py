# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.models import PredefinedModels

from . import dialog, model, view


class ModelsList(containers.DeclarativeContainer):
    """
    Container for creating widgets with a list of datasets.
    """

    Model = providers.Factory(model.ModelsListModel)
    View = providers.Factory(view.ModelsListView)

    Dialog = providers.Factory(dialog.ModelsListDialog, model=Model, view=View,)


class PredefinedModelsList(containers.DeclarativeContainer):
    """
    Container for creating a list with a list of predefined datasets.
    """

    Model = providers.Factory(
        model.ModelsListModel,
        models_list=[loader() for loader in PredefinedModels.providers.values()],
    )

    Dialog = providers.Factory(ModelsList.Dialog, model=Model)
