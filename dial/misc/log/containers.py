# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from .logger_dialog import LoggerDialog
from .logger_textbox import LoggerTextboxWidget

LoggerTextboxFactory = providers.Factory(LoggerTextboxWidget)

LoggerDialogFactory = providers.Factory(
    LoggerDialog, textbox_widget=LoggerTextboxFactory
)
