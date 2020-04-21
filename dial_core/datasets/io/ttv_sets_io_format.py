# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import os
from typing import Optional

import numpy as np

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import DataTypeContainer


class TTVSetsIOFormat:
    def save(self, root_path: str, name: str, dataset_desc: dict, dataset: "Dataset"):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        raise NotImplementedError()

    def load(self, root_path: str, dataset_desc: dict) -> "Dataset":
        """Loads the dataset from the file system.

        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_description dictionary (Data types, relative path...)

        Returns:
            The loaded dataset.
        """
        raise NotImplementedError()

    def __str__(self):
        return type(self).__name__


class NpzFormat(TTVSetsIOFormat):
    def save(self, root_path: str, name: str, dataset_desc: dict, dataset: "Dataset"):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_desc["path"] = f"{name}.npz"

        np.savez(
            root_path + os.path.sep + dataset_desc["path"], x=dataset._x, y=dataset._y
        )

    def load(self, root_path: str, dataset_desc: dict) -> Optional["Dataset"]:
        """Loads the dataset from the file system.
        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_desc dictionary (Data types, relative path...)
        """
        try:
            data = np.load(root_path + os.path.sep + dataset_desc["path"])

            x_type = getattr(DataTypeContainer, dataset_desc["x_type"])()
            y_type = getattr(DataTypeContainer, dataset_desc["y_type"])()

            return Dataset(data["x"], data["y"], x_type, y_type)

        except KeyError:
            return None


class TxtFormat(TTVSetsIOFormat):
    def save(self, root_path: str, name: str, dataset_desc: dict, dataset: "Dataset"):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_desc["x_path"] = f"{name}_x.txt"
        dataset_desc["y_path"] = f"{name}_y.txt"

        np.savetxt(root_path + os.path.sep + dataset_desc["x_path"], dataset._x)
        np.savetxt(root_path + os.path.sep + dataset_desc["y_path"], dataset._y)

    def load(self, root_path: str, dataset_desc: dict) -> Optional["Dataset"]:
        """Loads the dataset from the file system.
        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_desc dictionary (Data types, relative path...)
        """
        try:
            x = np.loadtxt(root_path + os.path.sep + dataset_desc["x_path"])
            y = np.loadtxt(root_path + os.path.sep + dataset_desc["y_path"])

            x_type = getattr(DataTypeContainer, dataset_desc["x_type"])()
            y_type = getattr(DataTypeContainer, dataset_desc["y_type"])()

            return Dataset(x, y, x_type, y_type)

        except KeyError:
            return None
