# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle


def test_project_attributes(project_a):
    assert hasattr(project_a, "name")
    assert hasattr(project_a, "file_path")
    assert hasattr(project_a, "scene")


def test_pickable(project_a):
    obj = pickle.dumps(project_a)

    loaded_project_a = pickle.loads(obj)

    assert loaded_project_a == project_a
