# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from unittest.mock import MagicMock, mock_open, patch

from dial_core.datasets.io import NpzFormat, TTVSetsIO


@patch("dial_core.datasets.io.ttv_sets_io.json", mock_json_dump=MagicMock())
@patch("builtins.open", new_callable=mock_open)
def test_save_ttv(mock_file_open, mock_json, ttv_sets):
    desc = TTVSetsIO.save(NpzFormat(), "foo/", ttv_sets)

    calls_list = mock_json.dump.call_args_list

    assert calls_list[0][0][0] == desc

    assert desc["train"]["x_type"] == ttv_sets.train.x_type.to_dict()
    assert desc["train"]["y_type"] == ttv_sets.train.x_type.to_dict()

    assert desc["test"]["x_type"] == ttv_sets.test.x_type.to_dict()
    assert desc["test"]["y_type"] == ttv_sets.test.x_type.to_dict()
