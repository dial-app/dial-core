# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
import re
from enum import Enum
from typing import Any, Optional

import dependency_injector.containers as containers
import dependency_injector.providers as providers
import numpy as np
from PIL import Image

from dial_core.datasets import Dataset
from dial_core.datasets.datatype import Categorical, DataType
from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class DatasetIO:
    """The TTVSetsIOFormat provides an interface for defining different formats in which
    a dataset could be stored on the file system."""

    Label = "DatasetIO"

    def __init__(self):
        self._dataset_description = {"x_type": {}, "y_type": {}}

        self._overrriden = {}

    def get_x_type(self) -> "DataType":
        return DataType.create(self._dataset_description["x_type"])

    def set_x_type(self, x_type: "DataType") -> "DatasetIO":
        self._set_attribute("x_type", x_type.to_dict())

        return self

    def get_y_type(self) -> "DataType":
        return DataType.create(self._dataset_description["y_type"])

    def set_y_type(self, y_type: "DataType") -> "DatasetIO":
        self._set_attribute("y_type", y_type.to_dict())

        return self

    def get_description(self) -> dict:
        return self._dataset_description

    def set_description(self, dataset_description: dict) -> "DatasetIO":
        self._dataset_description = dataset_description

        return self

    def save(self, parent_dir: str, dataset: "Dataset") -> dict:
        if not dataset:
            raise ValueError("Invalid dataset")

        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        self.set_x_type(dataset.x_type)
        self.set_y_type(dataset.y_type)

        return self._dataset_description

    def save_to_file(self, description_file_path: str, dataset: "Dataset",) -> dict:
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        parent_dir = os.path.dirname(description_file_path)

        self.save(parent_dir, dataset)

        with open(description_file_path, "w") as desc_file:
            json.dump(self._dataset_description, desc_file, indent=4)

        return self._dataset_description

    def load(self, parent_dir: str) -> "Dataset":
        """Loads the dataset from the specified `dataset_description` object. A
        `parent_dir` must be passed to resolve relative paths on the
        `dataset_description`.

        Returns:
            The loaded dataset.
        """
        x_type = self.get_x_type()
        y_type = self.get_y_type()

        # Dataset data (x, y) must be filled by subclasses overriding this method
        return Dataset(x_type=x_type, y_type=y_type)

    def load_from_file(self, description_file_path: str) -> Optional["Dataset"]:
        """Loads the dataset from the file system.

        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_description dictionary (Data types, relative path...)

        Returns:
            The loaded dataset.
        """
        with open(description_file_path, "r") as desc_file:
            self._dataset_description = json.load(desc_file)
            self._dataset_description.update(self._overrriden)
            self._overrriden = {}

        parent_dir = os.path.dirname(description_file_path)

        return self.load(parent_dir)

    def _set_attribute(self, attribute: str, value: Any):
        self._dataset_description[attribute] = value
        self._overrriden[attribute] = value

    def __str__(self) -> str:
        return self.Label


class NpzDatasetIO(DatasetIO):
    """The NpzFormat class stores datasets using Numpy's .npz files. See `np.savez` for
    more details."""

    Label = "Npz Format"

    def __init__(self):
        super().__init__()

        self.set_filename("output.npz")

    def get_filename(self) -> str:
        return self._dataset_description["filename"]

    def set_filename(self, filename: str) -> "NpzDatasetIO":
        self._set_attribute("filename", filename)

        return self

    def save(
        self, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        super().save(parent_dir, dataset)

        np.savez(
            os.path.join(parent_dir, self.get_filename()), x=dataset.x, y=dataset.y,
        )

        return self._dataset_description

    def load(self, parent_dir: str) -> Optional["Dataset"]:
        """Loads the dataset from the file system.
        Args:
            root_path: Path to the directory where the dataset file/dir is contained.
            dataset_desc: dataset_desc dictionary (Data types, relative path...)
        """
        dataset = super().load(parent_dir)

        npz_filepath = os.path.join(parent_dir, self.get_filename())

        if not npz_filepath:
            return None

        data = np.load(npz_filepath)
        dataset.x = data["x"]
        dataset.y = data["y"]

        return dataset


class TxtDatasetIO(DatasetIO):
    """The TxtFormat class stores datasets on plain readable .txt files."""

    Label = "Txt Format"

    def __init__(self):
        super().__init__()

        self.set_x_filename("x_output.txt")
        self.set_y_filename("y_output.txt")

    def get_x_filename(self) -> "TxtDatasetIO":
        return self._dataset_description["x_filename"]

    def set_x_filename(self, x_filename: str) -> "TxtDatasetIO":
        self._set_attribute("x_filename", x_filename)

        return self

    def get_y_filename(self) -> "TxtDatasetIO":
        return self._dataset_description["y_filename"]

    def set_y_filename(self, y_filename: str) -> "TxtDatasetIO":
        self._set_attribute("y_filename", y_filename)

        return self

    def save(
        self, parent_dir: str, dataset: "Dataset",
    ):
        """Writes the passed dataset to the file system.

        Args:
            root_path: Root directory where the dataset should be written to.
            name: Name of the output file/folder.
            dataset_desc: dataset_description dictionary (Data types, relative path...)
            dataset: Dataset to save.
        """
        super().save(parent_dir, dataset)

        np.savetxt(os.path.join(parent_dir, self.get_x_filename()), dataset.x)
        np.savetxt(os.path.join(parent_dir, self.get_y_filename()), dataset.y)

        return self._dataset_description

    def load(self, parent_dir: str) -> "Dataset":
        """"""
        dataset = super().load(parent_dir)

        dataset.x = np.loadtxt(os.path.join(parent_dir, self.get_x_filename()))
        dataset.y = np.loadtxt(os.path.join(parent_dir, self.get_y_filename()))

        return dataset


class CategoricalImgDatasetIO(DatasetIO):

    Label = "Categorical Images Format"

    class Organization(Enum):
        CategoryOnFolders = 0
        CategoryOnFilename = 1

    def __init__(self):
        super().__init__()

        self.set_organization(self.Organization.CategoryOnFolders)
        self.set_filename_category_regex(r"")

    def get_organization(self) -> "Organization":
        return self.Organization[self._dataset_description["organization"]]

    def set_organization(self, organization: "Organization"):
        self._set_attribute("organization", organization.name)

        return self

    def get_filename_category_regex(self) -> str:
        return self._dataset_description["filename_category_regex"]

    def set_filename_category_regex(self, filename_category_regex: str):
        self._set_attribute("filename_category_regex", filename_category_regex)

        return self

    def save(self, parent_dir: str, dataset: "Dataset"):
        super().save(parent_dir, dataset)

        num_zeros = len(str(len(dataset)))

        if self.get_organization() == self.Organization.CategoryOnFolders:
            # Create a folder for each category
            for category_idx in range(len(dataset.y_type.categories)):
                os.makedirs(os.path.join(parent_dir, str(category_idx)), exist_ok=True)

            for i, (x, y) in enumerate(zip(dataset.x, dataset.y)):
                im = Image.fromarray(x)
                im.save(
                    os.path.join(parent_dir, str(y), f"{str(i).zfill(num_zeros)}.png",)
                )

        elif self.get_organization() == self.Organization.CategoryOnFilename:
            for i, (x, y) in enumerate(zip(dataset.x, dataset.y)):
                im = Image.fromarray(x)
                im.save(
                    os.path.join(
                        parent_dir, f"{str(y)}__{str(i).zfill(num_zeros)}.png",
                    )
                )

        else:
            raise ValueError(f"Invalid organization value: {self.get_organization()}")

        return self._dataset_description

    def load(self, dataset_dir: str) -> "Dataset":
        category_extractor_regex = re.compile(self.get_filename_category_regex())

        dataset = super().load(dataset_dir)

        # Get categories if not defined
        if self.get_y_type() is None or len(self.get_y_type().categories) == 0:
            categorical_datatype = Categorical()

            if self.get_organization() == self.Organization.CategoryOnFolders:
                categorical_datatype.categories = os.listdir(dataset_dir)

            self.set_y_type(categorical_datatype)

        print("Categories", self.get_y_type().categories)

        # Load files
        x = []
        y = []

        if not dataset_dir:
            dataset.x = np.array(x)
            dataset.y = np.array(y)

            return dataset

        if self.get_organization() == self.Organization.CategoryOnFolders:
            for category_dir in os.listdir(dataset_dir):
                category_dir_full_path = os.path.join(dataset_dir, category_dir)

                if not os.path.isdir(category_dir_full_path):
                    continue

                category_data = self.get_y_type().convert_to_expected_format(
                    category_dir
                )

                for image_filename in os.listdir(category_dir_full_path):
                    image_full_path = os.path.join(
                        category_dir_full_path, image_filename
                    )

                    x.append(dataset.x_type.convert_to_expected_format(image_full_path))
                    y.append(category_data)

        elif self.get_organization() == self.Organization.CategoryOnFilename:
            for image_filename in os.listdir(os.path.join(dataset_dir)):
                try:
                    category_name = category_extractor_regex.match(
                        image_filename
                    ).group(1)

                    category_data = self.get_y_type().convert_to_expected_format(
                        category_name
                    )

                    image_full_path = os.path.join(dataset_dir, image_filename)

                    x.append(
                        self.get_x_type().convert_to_expected_format(image_full_path)
                    )
                    y.append(category_data)

                except Exception as err:
                    print(err)

        else:
            raise ValueError(f"Invalid organization value: {self.get_organization()}")

        dataset.x = np.array(x)
        dataset.y = np.array(y)

        return dataset


DatasetIORegistry = containers.DynamicContainer()
setattr(DatasetIORegistry, NpzDatasetIO.Label, providers.Factory(NpzDatasetIO))
setattr(DatasetIORegistry, TxtDatasetIO.Label, providers.Factory(TxtDatasetIO))
setattr(
    DatasetIORegistry,
    CategoricalImgDatasetIO.Label,
    providers.Factory(CategoricalImgDatasetIO),
)
