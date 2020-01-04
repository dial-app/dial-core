# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
# pylint: disable=C0103

"""
Widgets for displaying a logging window.
"""

import dependency_injector.providers as providers

from . import logger_dialog, logger_textbox

LoggerTextboxWidget = providers.Factory(logger_textbox.LoggerTextboxWidget)
LoggerDialog = providers.Factory(
    logger_dialog.LoggerDialog, textbox_widget=LoggerTextboxWidget
)

__all__ = ["LoggerDialog", "LoggerTextboxWidget"]
