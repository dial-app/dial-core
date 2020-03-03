# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial_core.project import Project


def test_default_project(project_manager, project_manager_default_project):
    # Check that they're NOT THE SAME OBJECT (ADDRESS)
    assert project_manager.active is not project_manager_default_project

    assert project_manager.active.name == project_manager_default_project.name


def test_add_new_project(project_manager):
    new_project_to_add = Project(name="New")

    project_manager.new_project(new_project_to_add)

    assert project_manager.active.name == new_project_to_add.name


def test_projects_count(project_manager):
    assert project_manager.projects_count() == 1

    project_manager.new_project()

    assert project_manager.projects_count() == 2


def test_set_active_project(project_manager, project_manager_default_project):
    new_project_to_add = Project(name="New")

    project_manager.new_project(new_project_to_add)

    project_manager.set_active_project(0)

    assert project_manager.active.name == project_manager_default_project.name

    project_manager.set_active_project(1)

    assert project_manager.active.name == new_project_to_add.name

    with pytest.raises(IndexError):
        project_manager.set_active_project(999999)


def test_save_project_without_file_path(project_manager):
    with pytest.raises(ValueError):
        project_manager.save_project()
