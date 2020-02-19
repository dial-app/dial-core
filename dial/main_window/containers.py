# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.providers as providers

from dial.misc.log import LoggerDialogFactory

from .main_menubar import MainMenuBar
from .main_window import MainWindow

MainMenuBarFactory = providers.Factory(MainMenuBar)

MainWindowFactory = providers.Factory(
    MainWindow, menubar=MainMenuBarFactory, logger_dialog=LoggerDialogFactory
)
