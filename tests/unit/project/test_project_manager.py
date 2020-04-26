# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import mock_open, patch

import pytest

import dial_core


def test_default_project(project_manager, project_manager_default_project):
    # Check that they're NOT THE SAME OBJECT (ADDRESS)
    assert project_manager.active is not project_manager_default_project

    assert project_manager.active.name == project_manager_default_project.name


def test_add_project(project_manager, project_a):
    project_manager.add_project(project_a)

    assert project_manager.active == project_a

    assert len(project_manager.projects) == 2


def test_projects_count(project_manager):
    assert project_manager.projects_count() == 1

    project_manager.new_project()

    assert project_manager.projects_count() == 2


def test_index_of(project_manager, project_a):
    project_manager.add_project(project_a)

    assert len(project_manager.projects) == 2
    assert project_manager.index_of(project_a) == 1

    assert project_manager.index_of(None) == -1


def test_set_active_project(
    project_manager, project_manager_default_project, project_a
):
    project_manager.add_project(project_a)

    project_manager.set_active_project(0)

    assert project_manager.active.name == project_manager_default_project.name

    project_manager.set_active_project(1)

    assert project_manager.active.name == project_a.name

    with pytest.raises(IndexError):
        project_manager.set_active_project(999999)


def test_close_project(project_manager, project_a):
    project_manager.add_project(project_a)

    assert project_manager.projects_count() == 2

    project_manager.close_project(project_a)

    assert project_manager.projects_count() == 1

    # Always has an active project
    project_manager.close_project(project_manager.active)

    assert project_manager.projects_count() == 1


@patch("builtins.open", new_callable=mock_open)
@patch.object(dial_core.project.project_manager.pickle, "load")
def test_open_project(mock_pickle_load, mock_file_open, project_manager):
    # Open a (mocked) file from the system and return the new project
    file_path = "foo.dial"
    opened_project = project_manager.open_project(file_path)

    # Check that the file was read from system and that load was called
    opened_file_binary = mock_file_open.return_value
    mock_pickle_load.assert_called_once_with(opened_file_binary)

    # Check that the project was created successfully
    assert opened_project.file_path == file_path

    # Check that the new opened project is the active project
    assert project_manager.active == opened_project


@patch("builtins.open", new_callable=mock_open)
def test_open_inexistent_project(mock_file_open, project_manager):
    mock_file_open.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError):
        project_manager.open_project("foo.txt")


@patch("builtins.open", new_callable=mock_open)
@patch.object(dial_core.project.project_manager.pickle, "dump")
def test_save_project(mock_pickle_dump, mock_file_open, project_manager):
    project_manager.active.file_path = "foo.dial"

    opened_file_binary = mock_file_open.return_value

    project_manager.save_project(project_manager.active)

    mock_pickle_dump.assert_called_once_with(project_manager.active, opened_file_binary)


def test_save_project_without_file_path(project_manager):
    with pytest.raises(ValueError):
        project_manager.save_project(project_manager.active)


@patch("builtins.open", new_callable=mock_open)
def test_save_project_as(_, project_manager):
    assert not project_manager.active.file_path

    project_manager.save_project_as(project_manager.active, "foo_dir")

    assert project_manager.active.file_path == "foo_dir/TestProject/TestProject.dial"
