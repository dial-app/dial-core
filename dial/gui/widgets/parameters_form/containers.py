# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from . import parameters_form

ParametersFormFactory = providers.Factory(parameters_form.ParametersForm)
