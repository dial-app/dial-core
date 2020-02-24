# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .model_compiler_node import ModelCompilerNode
from .model_compiler_widget import ModelCompilerWidget
from .parameters_form import ParametersFormFactory

ModelCompilerWidgetFactory = providers.Factory(
    ModelCompilerWidget, parameters_form=ParametersFormFactory
)

ModelCompilerNodeFactory = providers.Factory(
    ModelCompilerNode, model_compiler_widget=ModelCompilerWidgetFactory
)
