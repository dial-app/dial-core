# # vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:
#
# from PySide2.QtCore import QObject, Signal
#
# from dial.project.project import DatasetInfo, ModelInfo, Project
#
#
# class ProjectQt(QObject, Project):
#     """
#     Dial project file with Qt Signals.
#     """
#
#     dataset_changed = Signal(QObject)
#     model_changed = Signal(QObject)
#
#     def __init__(self, default_dataset_info, default_model_info):
#         super().__init__(default_dataset_info, default_model_info)
#
#         self.dataset.dataset_changed.connect(lambda: self.dataset_changed.emit(self))
#         self.model.model_changed.connect(lambda: self.model_changed.emit(self))
#
#
# class DatasetInfoQt(QObject, DatasetInfo):
#     """
#     DatasetInfo class with Qt Signals.
#     """
#
#     dataset_changed = Signal()
#
#     def __init__(self):
#         super().__init__()
#
#     def load_dataset(self, dataset_loader):
#         super().load_dataset(dataset_loader)
#
#         self.dataset_changed.emit()
#
#
# class ModelInfoQt(QObject, ModelInfo):
#     """
#     ModelInfo class with Qt Signals.
#     """
#
#     model_changed = Signal()
#
#     def __init__(self):
#         super().__init__()
#
#     def load_model(self, model_loader):
#         super().load_model(model_loader)
#
#         self.model_changed.emit()
