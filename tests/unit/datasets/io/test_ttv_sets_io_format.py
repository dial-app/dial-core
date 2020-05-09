# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from unittest.mock import MagicMock, patch

from dial_core.datasets.io import NpzFormat


@patch("dial_core.datasets.io.ttv_sets_io_format.np.savez", mock_json_dump=MagicMock())
def test_npz_save_to_description(npz_savez_mock, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = NpzFormat.save_to_description(
        identifier, parent_dir, train_dataset
    )

    assert dataset_description["filename"] == f"{identifier}.npz"
    assert dataset_description["x_type"] == train_dataset.x_type.to_dict()
    assert dataset_description["y_type"] == train_dataset.y_type.to_dict()

    npz_savez_mock.assert_called_once_with(
        parent_dir + os.path.sep + f"{identifier}.npz",
        x=train_dataset.x,
        y=train_dataset.y,
    )


@patch("dial_core.datasets.io.ttv_sets_io_format.np.load", mock_json_dump=MagicMock())
def test_npz_load_from_description(np_load_mock, train_dataset):
    identifier = "train"
    parent_dir = "foo"

    dataset_description = {
        "filename": f"{identifier}.npz",
        "x_type": train_dataset.x_type.to_dict(),
        "y_type": train_dataset.y_type.to_dict(),
    }

    np_load_mock.load.side_effect = {"x": train_dataset.x, "y": train_dataset.y}

    loaded_dataset = NpzFormat.load_from_description(parent_dir, dataset_description)

    np_load_mock.assert_called_once_with(
        parent_dir + os.path.sep + dataset_description["filename"]
    )

    assert loaded_dataset.x.all(train_dataset.x)
    assert loaded_dataset.y.all(train_dataset.y)
