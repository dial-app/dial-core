# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Widgets for displaying a dataset content with Train/Test tabs.
"""

from .dataset_table_model import DatasetTableModel
from .dataset_table_view import DatasetTableView
from .train_test_tabs import TrainTestTabs

__all__ = [
    "DatasetTableModel",
    "DatasetTableView",
    "TrainTestTabs",
]
