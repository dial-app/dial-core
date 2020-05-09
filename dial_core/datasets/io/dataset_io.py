# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import Optional

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import numpy as np
from PIL import Image

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import Categorical, DataTypeContainer, ImageArray
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class DatasetIO:
    """The TTVSetsIOFormat provides an interface for defining different formats in which
    a dataset could be stored on the file system."""

    @classmethod
    def save(
        cls, identifier: str, description_file_path: str, dataset: "Dataset",
    ) -> dict:
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        parent_dir = os.path.dirname(description_file_path)

        dataset_description = cls.save_to_description(identifier, parent_dir, dataset)
        print(dataset_description)

        with open(description_file_path, "w") as desc_file:
            json.dump(dataset_description, desc_file, indent=4)

        return dataset_description

    @classmethod
    def save_to_description(
        cls, identifier: str, parent_dir: str, dataset: "Dataset"
    ) -> dict:
        if not dataset:
            raise ValueError("Invalid dataset")

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        dataset_description = {}
        dataset_description["x_type"] = dataset.x_type.to_dict()
        dataset_description["y_type"] = dataset.y_type.to_dict()

        return dataset_description

    @classmethod
    def load(cls, description_file_path: str) -> Optional["Dataset"]:
        """Loads the dataset from the file system.

        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_description dictionary (Data types, relative path...)

        Returns:
            The loaded dataset.
        """
        with open(description_file_path, "r") as desc_file:
            dataset_description = json.load(desc_file)

        parent_dir = os.path.dirname(description_file_path)

        return cls.load_from_description(parent_dir, dataset_description)

    @classmethod
    def load_from_description(
        cls, parent_dir: str, dataset_description: dict
    ) -> "Dataset":
        """Loads the dataset from the specified `dataset_description` object. A
        `parent_dir` must be passed to resolve relative paths on the
        `dataset_description`.

        Returns:
            The loaded dataset.
        """
        x_type = getattr(
            DataTypeContainer, dataset_description["x_type"]["class"]
        )().from_dict(dataset_description["x_type"])

        y_type = getattr(
            DataTypeContainer, dataset_description["y_type"]["class"]
        )().from_dict(dataset_description["y_type"])

        # Dataset data (x, y) must be filled by subclasses overriding this method
        return Dataset(x_type=x_type, y_type=y_type)

    def __str__(self):
        return type(self).__name__


class NpzDatasetIO(DatasetIO):
    """The NpzFormat class stores datasets using Numpy's .npz files. See `np.savez` for
    more details."""

    @classmethod
    def save_to_description(
        cls, identifier: str, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_description = super().save_to_description(
            identifier, parent_dir, dataset
        )

        dataset_description["filename"] = f"{identifier}.npz"

        np.savez(
            os.path.join(parent_dir, dataset_description["filename"]),
            x=dataset.x,
            y=dataset.y,
        )

        return dataset_description

    @classmethod
    def load_from_description(
        cls, parent_dir: str, dataset_description: dict
    ) -> Optional["Dataset"]:
        """Loads the dataset from the file system.
        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_desc dictionary (Data types, relative path...)
        """
        dataset = super().load_from_description(parent_dir, dataset_description)

        data = np.load(os.path.join(parent_dir, dataset_description["filename"]))

        dataset.x = data["x"]
        dataset.y = data["y"]

        return dataset


class TxtDatasetIO(DatasetIO):
    """The TxtFormat class stores datasets on plain readable .txt files."""

    @classmethod
    def save_to_description(
        cls, identifier: str, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        dataset_description = super().save_to_description(
            identifier, parent_dir, dataset
        )

        dataset_description["x_filename"] = f"x_{identifier}.txt"
        dataset_description["y_filename"] = f"y_{identifier}.txt"

        np.savetxt(
            os.path.join(parent_dir, dataset_description["x_filename"]), dataset.x,
        )
        np.savetxt(
            os.path.join(parent_dir, dataset_description["y_filename"]), dataset.y,
        )

        return dataset_description

    @classmethod
    def load_from_description(
        cls, parent_dir: str, dataset_description: dict
    ) -> "Dataset":
        """"""
        dataset = super().load_from_description(parent_dir, dataset_description)

        dataset.x = np.loadtxt(
            os.path.join(parent_dir, dataset_description["x_filename"])
        )

        dataset.y = np.loadtxt(
            os.path.join(parent_dir, dataset_description["y_filename"])
        )

        return dataset


class CategoricalImgDatasetIO(DatasetIO):
    @classmethod
    def save_to_description(cls, identifier: str, parent_dir: str, dataset: "Dataset"):
        dataset_description = super().save_to_description(
            identifier, parent_dir, dataset
        )

        for category in dataset.y_type.categories:
            os.makedirs(os.path.join(parent_dir, category), exist_ok=True)

        num_zeros = len(str(len(dataset)))

        for i, (x, y) in enumerate(zip(dataset.x, dataset.y)):
            im = Image.fromarray(x)
            im.save(
                os.path.join(
                    parent_dir,
                    str(dataset.y_type.display(y)),
                    f"{str(i).zfill(num_zeros)}.png",
                )
            )

        return dataset_description

    @classmethod
    def load_from_description(
        cls, parent_dir: str, dataset_description: dict
    ) -> Optional["Dataset"]:
        print(os.listdir(parent_dir))
        x = []
        y = []

        x_type = ImageArray()
        y_type = Categorical(categories=os.listdir(parent_dir))

        for category_dir in os.listdir(parent_dir):
            for image in os.listdir(os.path.join(parent_dir, category_dir)):
                print(os.path.join(parent_dir, category_dir, image))
                image = Image.open(os.path.join(parent_dir, category_dir, image))

                x.append(np.array(image))
                y.append(category_dir)

                image.close()

        return Dataset(
            x_data=np.array(x), y_data=np.array(y), x_type=x_type, y_type=y_type
        )


DatasetIOContainer = containers.DynamicContainer()
DatasetIOContainer.NpzDatasetIO = providers.Factory(NpzDatasetIO)
DatasetIOContainer.TxtDatasetIO = providers.Factory(TxtDatasetIO)
DatasetIOContainer.CategoricalImgDatasetIO = providers.Factory(CategoricalImgDatasetIO)
