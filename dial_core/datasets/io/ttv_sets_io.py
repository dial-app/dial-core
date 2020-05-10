# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import TYPE_CHECKING, Optional

from dial_core.datasets import TTVSets
from dial_core.datasets.io import DatasetIORegistry

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
    def save_to_file(
        cls, description_file_path: str, dataset_io: "DatasetIO", ttv_sets: "TTVSets",
    ) -> dict:
        # Save all datasets inside this directory
        ttv_dir = os.path.dirname(description_file_path)

        if not os.path.exists(ttv_dir):
            os.makedirs(ttv_dir, exist_ok=True)

        ttv_description = cls.save_to_description(ttv_dir, dataset_io, ttv_sets)

        # Writes the datasets structure on a json file
        with open(description_file_path, "w") as desc_file:
            json.dump(ttv_description, desc_file, indent=4)

        return ttv_description

    @classmethod
    def save_to_description(
        self, ttv_dir: str, dataset_io: "DatasetIO", ttv_sets: "TTVSets"
    ):
        def save_dataset(dataset_dir, dataset):
            return (
                dataset_io.save(os.path.join(ttv_dir, dataset_dir), dataset)
                if dataset
                else {}
            )

        return {
            "name": ttv_sets.name,
            "format": str(dataset_io),
            "train": save_dataset("train", ttv_sets.train),
            "test": save_dataset("test", ttv_sets.test),
            "validation": save_dataset("validation", ttv_sets.validation),
        }

    @classmethod
    def load_from_file(
        cls, description_file_path: str, dataset_io_providers=DatasetIORegistry,
    ) -> "TTVSets":
        ttv_dir = os.path.dirname(description_file_path)
        ttv_description = cls.load_ttv_description(description_file_path)

        return cls.load_from_description(ttv_dir, ttv_description, dataset_io_providers)

    @classmethod
    def load_from_description(
        cls,
        ttv_dir: str,
        ttv_description: dict,
        dataset_io_providers=DatasetIORegistry,
    ) -> "TTVSets":

        dataset_io = getattr(dataset_io_providers, ttv_description["format"])

        def load_dataset(dataset_dir, dataset_description):
            return (
                dataset_io.set_description(dataset_description).load(
                    os.path.join(ttv_dir, dataset_dir)
                )
                if dataset_description
                else None
            )

        train = load_dataset("train", ttv_description["train"])
        test = load_dataset("test", ttv_description["test"])
        validation = load_dataset("validation", ttv_description["validation"])

        return TTVSets(ttv_description["name"], train, test, validation)

    @classmethod
    def load_ttv_description(cls, description_file_path: str) -> Optional[dict]:
        with open(description_file_path, "r") as desc_file:
            return json.load(desc_file)

        return None
