# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_ttv_sets_to_dict(ttv_sets):
    dc = ttv_sets.to_dict()

    assert dc["dataset"]["name"] == ttv_sets.name
    assert dc["train"]["x_type"] == ttv_sets.train.x_type.to_dict()
    assert dc["train"]["y_type"] == ttv_sets.train.y_type.to_dict()
    assert dc["test"]["x_type"] == ttv_sets.test.x_type.to_dict()
    assert dc["test"]["y_type"] == ttv_sets.test.y_type.to_dict()
    assert dc["validation"] == {}
