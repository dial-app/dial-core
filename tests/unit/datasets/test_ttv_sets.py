# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_ttv_sets_to_dict(ttv_sets):
    dc = ttv_sets.to_dict()

    assert dc["dataset"]["name"] == ttv_sets.name
    assert dc["train"]["x_type"] == str(ttv_sets.train.x_type)
    assert dc["train"]["y_type"] == str(ttv_sets.train.y_type)
    assert dc["test"]["x_type"] == str(ttv_sets.test.x_type)
    assert dc["test"]["y_type"] == str(ttv_sets.test.y_type)
    assert dc["validation"] == {}
