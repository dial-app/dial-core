# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import TYPE_CHECKING

from dial_core.datasets import TTVSets
from dial_core.datasets.io import DatasetIOContainer

if TYPE_CHECKING:
    from .ttv_sets_io_format import DatasetIO


class TTVSetsIO:
    """The TTVSetsIO class provides an interface for saving/loading TTVSets classes
    from/to memory. The format used for the stored elements (files, directories, npz
    files..) depends on the `io_format` argument.

    For more information about how each `dataset_io` works, see the `DatasetIO`
    class.
    """

    @classmethod
    def save(
        cls, parent_dir: str, dataset_io: "DatasetIO", ttv_sets: "TTVSets",
    ) -> dict:
        """Saves a TTVSets object on the file system.

        Depending on the passed `io_format`, the files structure will be different, but
        all datasets must have a `description.json` file defining the general structure
        of the Dataset: name, description, paths to train/test/validation datasets (if
        any), datatypes used...

        Args:
            io_format: Format in which the datasets will be stored.
            parent_path: Directory where the dataset will be created.

        Returns:
            The saved dictionary with the ttv_sets information
        """
        # Save all datasets inside this directory
        ttv_dir = os.path.join(parent_dir, ttv_sets.name)

        if not os.path.exists(ttv_dir):
            os.makedirs(ttv_dir, exist_ok=True)

        ttv_description = cls.save_to_description(ttv_dir, dataset_io, ttv_sets)

        # Writes the datasets structure on a json file
        with open(os.path.join(ttv_dir, "ttv_description.json"), "w") as desc_file:
            json.dump(ttv_description, desc_file, indent=4)

        return ttv_description

    @classmethod
    def save_to_description(
        self, parent_dir: str, dataset_io: "DatasetIO", ttv_sets: "TTVSets"
    ):
        def save_dataset(identifier, dataset):
            return (
                dataset_io.save_to_description(
                    identifier, os.path.join(parent_dir, identifier), dataset
                )
                if dataset
                else {}
            )

        return {
            "name": ttv_sets.name,
            "format": dataset_io.__name__,
            "train": save_dataset("train", ttv_sets.train),
            "test": save_dataset("test", ttv_sets.test),
            "validation": save_dataset("validation", ttv_sets.validation),
        }

    @classmethod
    def load(cls, ttv_dir: str, dataset_io_providers=DatasetIOContainer) -> "TTVSets":
        """Loads a DatasetsGroup from the file system.

        This method will first find the `description.json` file inside the dataset
        directory. This file has the whole structure of the datasets and how to locate
        the necessary files, along with which io_formats use.
        """
        with open(os.path.join(ttv_dir, "ttv_description.json"), "r") as desc_file:
            ttv_description = json.load(desc_file)

        dataset_io = getattr(dataset_io_providers, ttv_description["format"])()

        def load_dataset(identifier, dataset_description):
            return (
                dataset_io.load_from_description(
                    os.path.join(ttv_dir, identifier), dataset_description,
                )
                if dataset_description
                else None
            )

        train = load_dataset("train", ttv_description["train"])
        test = load_dataset("test", ttv_description["test"])
        validation = load_dataset("validation", ttv_description["validation"])

        return TTVSets(
            name=ttv_description["name"], train=train, test=test, validation=validation,
        )
