# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import json
import os

import numpy as np

from dial_core.datasets import Dataset, DatasetsContainer
from dial_core.datasets.datatype import DataTypeContainer

# For a dataset like:

# ImageArray    Categorical

# Save as:

# train.npz
# test.npz
# details.json
# {
#   "dataset": {
#     "name": "MNIST",
#   },
#   "train": {
#     "path": "train.npz",
#     "x_type": "ImageArray",
#     "y_type": "Categorical"
#   },
#   "test": {
#     "path": "train.npz",
#     "x_type": "ImageArray",
#     "y_type": "Categorical"
#   },
#   # "validation": {
#   # }
# }
#


class DatasetExporter:
    def export(self, path: str, datasets_container):
        root_datasets_dir = path + os.path.sep + datasets_container.name + os.path.sep
        if not os.path.isdir(root_datasets_dir):
            os.mkdir(root_datasets_dir)

        desc = {
            "dataset": {"name": datasets_container.name},
            "train": {
                "path": "train.npz",
                "format": "npz",
                "x_type": str(datasets_container.train.x_type),
                "y_type": str(datasets_container.train.y_type),
            },
            "test": {
                "path": "test.npz",
                "format": "npz",
                "x_type": str(datasets_container.test.x_type),
                "y_type": str(datasets_container.test.y_type),
            },
        }

        export_to_npz(root_datasets_dir, desc["train"], datasets_container.train)
        export_to_npz(root_datasets_dir, desc["test"], datasets_container.test)

        with open(root_datasets_dir + "description.json", "w") as desc_file:
            json.dump(desc, desc_file, indent=2)

    def import_dataset(self, root_datasets_dir: str):
        with open(
            root_datasets_dir + os.path.sep + "description.json", "r"
        ) as desc_file:
            content = json.load(desc_file)

            train = import_from_npz(root_datasets_dir, content["train"])
            test = import_from_npz(root_datasets_dir, content["test"])

            return DatasetsContainer(content["dataset"]["name"], train, test)


def export_to_npz(root_path: str, dataset_desc: str, dataset: "Dataset"):
    np.savez(root_path + os.path.sep + dataset_desc["path"], x=dataset._x, y=dataset._y)


def import_from_npz(root_path: str, dataset_desc: str):
    data = np.load(root_path + os.path.sep + dataset_desc["path"])

    x_type = getattr(DataTypeContainer, dataset_desc["x_type"])()
    y_type = getattr(DataTypeContainer, dataset_desc["y_type"])()

    return Dataset(data["x"], data["y"], x_type, y_type)
