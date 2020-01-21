# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.gui.widgets import Logger, MenuBars, TrainTestTabs

from . import datasets_window, main_window, models_window


class Windows(containers.DeclarativeContainer):
    """
    Container for creating window instances.
    """

    Datasets = providers.Factory(
        datasets_window.DatasetsWindow, dataset_table_widget=TrainTestTabs()
    )

    Models = providers.Factory(models_window.ModelsWindow)

    Main = providers.Factory(
        main_window.MainWindow, Datasets, Models, MenuBars.Main, Logger.Dialog
    )
