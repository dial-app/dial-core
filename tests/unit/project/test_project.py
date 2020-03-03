# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle

import pytest


def test_project_attributes(project_a):
    assert hasattr(project_a, "name")
    assert hasattr(project_a, "file_path")
    assert hasattr(project_a, "scene")


def test_is_pickable(project_a):
    try:
        pickle.dumps(project_a)
    except pickle.PicklingError:
        pytest.fail("Project is not pickable.")
