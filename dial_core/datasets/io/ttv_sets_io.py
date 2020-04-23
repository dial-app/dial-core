# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os
from typing import TYPE_CHECKING

from dial_core.datasets import TTVSets

if TYPE_CHECKING:
    from .ttv_sets_io_format import TTVSetsIOFormat


class TTVSetsIO:
    """This class provides an interface for saving/loading TTVSets classes from/to
    memory. The format used for the stored elements (files, directories, npz files..)
    depends on the `io_format` argument.

    For more information about how each `io_format` works, see the `TTVSetsIOFormat`
    class.
    """

    @classmethod
    def save(
        cls, io_format: "TTVSetsIOFormat", save_path: str, ttv_sets: "TTVSets",
        override=False
    ):
        """Saves a TTVSets object on the file system.

        Depending on the passed `io_format`, the files structure will be different, but
        all datasets must have a `description.json` file defining the general structure
        of the Dataset: name, description, paths to train/test/validation datasets (if
        any), datatypes used...
        """
        # Save all datasets inside this directory
        root_dir = save_path + os.path.sep + ttv_sets.name + os.path.sep

        if not os.path.isdir(root_dir):
            os.mkdir(root_dir)
        elif not override:
            print("Returning without overriding")
            return

        desc = ttv_sets.to_dict()
        desc["format"] = str(io_format)  # Must store the format for loading later

        if ttv_sets.train:
            io_format.save(root_dir, "train", desc["train"], ttv_sets.train)

        if ttv_sets.test:
            io_format.save(root_dir, "test", desc["test"], ttv_sets.test)

        if ttv_sets.validation:
            io_format.save(
                root_dir, "validation", desc["validation"], ttv_sets.valvalidation
            )

        # Writes the datasets structure on a json file
        with open(root_dir + os.path.sep + "description.json", "w") as desc_file:
            json.dump(desc, desc_file, indent=4)

    @classmethod
    def load(cls, load_path: str, dataset_io_formats) -> "TTVSets":
        """Loads a DatasetsGroup from the file system.

        This method will first find the `description.json` file inside the dataset
        directory. This file has the whole structure of the datasets and how to locate
        the necessary files, along with which io_formats use.
        """
        with open(load_path + os.path.sep + "description.json", "r") as desc_file:
            desc = json.load(desc_file)

            io_format = getattr(dataset_io_formats, desc["format"])()

            train = io_format.load(load_path, desc["train"])
            test = io_format.load(load_path, desc["test"])
            validation = io_format.load(load_path, desc["validation"])

            return TTVSets(
                name=desc["dataset"]["name"],
                train=train,
                test=test,
                validation=validation,
            )
