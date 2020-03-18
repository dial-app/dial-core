# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial_core.node_editor import SceneFactory

from .project import Project
from .project_manager import ProjectManager

DefaultProject = providers.Factory(Project, name="Default Project", scene=SceneFactory)

ProjectManagerFactory = providers.Factory(
    ProjectManager, default_project=DefaultProject
)

ProjectManagerSingleton = providers.Singleton(
    ProjectManager, default_project=DefaultProject
)
