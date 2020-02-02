# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from PySide2.QtCore import QObject, Slot

from dial.project import Project, ProjectManager
from dial.utils import log

LOGGER = log.get_logger(__name__)


class ProjectManagerQt(QObject, ProjectManager):
    def __init__(self, default_project: Project):
        super().__init__()

    @Slot()
    def new_project(self):
        super().new_project()
