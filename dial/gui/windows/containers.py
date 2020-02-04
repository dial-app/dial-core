# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Dependency Injection containers.
"""

import dependency_injector.containers as containers
import dependency_injector.providers as providers

from dial.gui.widgets import (
    LayersTree,
    Logger,
    MenuBars,
    ModelTable,
    ParametersFormFactory,
    TrainTestTable,
)
from dial.project import DialProjectManager

from . import compile_window, datasets_window, main_window, models_window, train_window


class Windows(containers.DeclarativeContainer):
    """
    Container for creating window instances.
    """

    Datasets = providers.Factory(
        datasets_window.DatasetsWindow,
        project_manager=DialProjectManager,
        dataset_table_widget=TrainTestTable.Widget,
    )

    Models = providers.Factory(
        models_window.ModelsWindow,
        project_manager=DialProjectManager,
        layers_tree=LayersTree.Widget,
        model_table=ModelTable.Widget,
    )

    Compile = providers.Factory(
        compile_window.CompileWindow,
        project_manager=DialProjectManager,
        parameters_form=ParametersFormFactory,
    )

    Train = providers.Factory(
        train_window.TrainWindow, project_manager=DialProjectManager
    )

    Main = providers.Factory(
        main_window.MainWindow,
        project_manager=DialProjectManager,
        datasets_window=Datasets,
        models_window=Models,
        compile_window=Compile,
        train_window=Train,
        menubar=MenuBars.Main,
        logger_dialog=Logger.Dialog,
    )
