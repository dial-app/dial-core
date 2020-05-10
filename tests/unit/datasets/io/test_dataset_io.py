# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from unittest.mock import patch

from dial_core.datasets.io import NpzDatasetIO, TxtDatasetIO


@patch("dial_core.datasets.io.dataset_io.np")
def test_npz_save(mock_np, train_dataset):
    filename = "train.npz"
    parent_dir = "foo"

    dataset_description = (
        NpzDatasetIO().set_filename(filename).save(parent_dir, train_dataset)
    )

    assert dataset_description["filename"] == filename
    assert dataset_description["x_type"] == train_dataset.x_type.to_dict()
    assert dataset_description["y_type"] == train_dataset.y_type.to_dict()

    mock_np.savez.assert_called_once_with(
        os.path.join(parent_dir, filename), x=train_dataset.x, y=train_dataset.y,
    )


@patch("dial_core.datasets.io.dataset_io.np")
def test_npz_load(mock_np, train_dataset):
    parent_dir = "foo"

    dataset_description = {
        "filename": "filename.npz",
        "x_type": train_dataset.x_type.to_dict(),
        "y_type": train_dataset.y_type.to_dict(),
    }

    mock_np.load.side_effect = [{"x": train_dataset.x, "y": train_dataset.y}]

    loaded_dataset = (
        NpzDatasetIO().set_description(dataset_description).load(parent_dir)
    )

    mock_np.load.assert_called_once_with(
        os.path.join(parent_dir, dataset_description["filename"])
    )

    assert loaded_dataset.x.tolist() == train_dataset.x.tolist()
    assert loaded_dataset.y.tolist() == train_dataset.y.tolist()


@patch("dial_core.datasets.io.dataset_io.np")
def test_txt_save(mock_np, train_dataset):
    x_filename = "x_train.txt"
    y_filename = "y_train.txt"
    parent_dir = "foo"

    dataset_description = (
        TxtDatasetIO()
        .set_x_filename(x_filename)
        .set_y_filename(y_filename)
        .save(parent_dir, train_dataset)
    )

    calls_list = mock_np.savetxt.call_args_list

    assert calls_list[0][0] == (os.path.join(parent_dir, x_filename), train_dataset.x,)
    assert calls_list[1][0] == (os.path.join(parent_dir, y_filename), train_dataset.y,)

    assert dataset_description["x_filename"] == x_filename
    assert dataset_description["y_filename"] == y_filename
    assert dataset_description["x_type"] == train_dataset.x_type.to_dict()
    assert dataset_description["y_type"] == train_dataset.y_type.to_dict()


@patch("dial_core.datasets.io.dataset_io.np")
def test_txt_load(mock_np, train_dataset):
    parent_dir = "foo"

    dataset_description = {
        "x_filename": f"x_train.txt",
        "y_filename": f"y_train.txt",
        "x_type": train_dataset.x_type.to_dict(),
        "y_type": train_dataset.y_type.to_dict(),
    }

    mock_np.loadtxt.side_effect = [train_dataset.x, train_dataset.y]

    loaded_dataset = (
        TxtDatasetIO().set_description(dataset_description).load(parent_dir)
    )

    calls_list = mock_np.loadtxt.call_args_list
    assert calls_list[0][0] == (
        os.path.join(parent_dir, dataset_description["x_filename"]),
    )
    assert calls_list[1][0] == (
        os.path.join(parent_dir, dataset_description["y_filename"]),
    )

    assert loaded_dataset.x.tolist() == train_dataset.x.tolist()
    assert loaded_dataset.y.tolist() == train_dataset.y.tolist()
