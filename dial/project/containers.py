# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from . import project, project_manager
from .qt import ProjectManagerQt

DatasetInfo = providers.Factory(project.DatasetInfo)
ModelInfo = providers.Factory(project.ModelInfo)

Project = providers.Factory(
    project.Project, default_dataset_info=DatasetInfo, default_model_info=ModelInfo,
)

ProjectManager = providers.Factory(
    project_manager.ProjectManager, default_project=Project
)

DialProjectManager = providers.Singleton(ProjectManagerQt, default_project=Project)
