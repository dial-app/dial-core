# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .node_factory import NodeFactory
from .scene import Scene

DefaultSceneFactory = providers.Factory(Scene)

NodeFactorySingleton = providers.Singleton(NodeFactory)
