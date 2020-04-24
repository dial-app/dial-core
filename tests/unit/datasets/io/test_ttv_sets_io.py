# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.datasets.io import NpzFormat, TTVSetsIO


# @patch("builtins.open", new_callable=mock_open)
def test_save_ttv(ttv_sets):
    TTVSetsIO.save(NpzFormat(), "foo/", ttv_sets)
