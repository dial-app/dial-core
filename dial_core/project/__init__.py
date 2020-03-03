# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
The project package provides classes for storing and managing projects: Sets of scenes
and configurations that can be stored and loaded.
"""

from .containers import ProjectManagerFactory, ProjectManagerSingleton
from .project import Project
from .project_manager import ProjectManager

__all__ = [
    "Project",
    "ProjectManager",
    "ProjectManagerSingleton",
    "ProjectManagerFactory",
]
