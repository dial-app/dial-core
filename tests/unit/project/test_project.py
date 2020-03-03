# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


def test_project_attributes(default_project):
    assert hasattr(default_project, "name")
    assert hasattr(default_project, "file_path")
    assert hasattr(default_project, "scene")


def test_is_pickable(default_project):
    try:
        pickle.dumps(default_project)
    except pickle.PicklingError:
        pytest.fail("Project is not pickable.")
