# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""This package has the basic nodes that can be placed on the Node Editor.

From editing datasets to compiling models, this nodes should satisfy most of the needs
when working with classical Deep Learning problems.
"""

from dial.node_editor import NodeFactorySingleton

from .dataset_editor import DatasetEditorNodeFactory
from .layers_editor import LayersEditorNodeFactory
from .model_compiler import ModelCompilerNodeFactory

NodeFactorySingleton().register_node_factory("Dataset Editor", DatasetEditorNodeFactory)
NodeFactorySingleton().register_node_factory("Layers Editor", LayersEditorNodeFactory)
NodeFactorySingleton().register_node_factory("Model Compiler", ModelCompilerNodeFactory)
