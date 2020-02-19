# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from .layers_tree_model import LayersTreeModel
from .layers_tree_view import LayersTreeView
from .layers_tree_widget import LayersTreeWidget


class LayersTreeMVFactory(containers.DeclarativeContainer):
    Model = providers.Factory(LayersTreeModel)
    View = providers.Factory(LayersTreeView)


LayersTreeFactory = providers.Factory(
    LayersTreeWidget, layerstree_mv_factory=LayersTreeMVFactory
)
