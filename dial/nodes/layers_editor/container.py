# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .layers_editor_node import LayersEditorNode
from .layers_editor_widget import LayersEditorWidget
from .layers_tree import LayersTreeFactory
from .model_table import ModelTableFactory

LayersEditorWidgetFactory = providers.Factory(
    LayersEditorWidget, layers_tree=LayersTreeFactory, model_table=ModelTableFactory
)

LayersEditorNodeFactory = providers.Factory(
    LayersEditorNode, layers_editor_widget=LayersEditorWidgetFactory
)
