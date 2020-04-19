# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Optional

from dial_core.datasets import Dataset


class DatasetsContainer:
    def __init__(
        self,
        name: str,
        train: "Dataset",
        test: "Dataset",
        validation: Optional["Dataset"] = None,
    ):
        self.name = name
        self.train = train
        self.test = test
        self.validation = validation
