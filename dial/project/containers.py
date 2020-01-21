# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from . import project

Project = providers.Factory(project.Project)

ProjectInstance = providers.Singleton(Project)
