# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widgets for displaying a dataset content with Train/Test tabs.
"""

import dependency_injector.providers as providers

from . import train_test_tabs

TrainTestTabs = providers.Factory(train_test_tabs.TrainTestTabs)

__all__ = [
    "TrainTestTabs",
]
