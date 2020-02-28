# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .project import Project
from .project_manager import ProjectManager

ProjectManagerSingleton = providers.Singleton(ProjectManager, default_project=Project())
