# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.gui.widgets import Logger, MenuBars

from . import main_window


class Windows(containers.DeclarativeContainer):
    """
    Container for creating window instances.
    """

    Main = providers.Factory(
        main_window.MainWindow, menubar=MenuBars.Main, logger_dialog=Logger.Dialog,
    )
