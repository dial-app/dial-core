# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.datasets import TTVSets
from dial_core.datasets.io import TTVSetsFormatsContainer, TTVSetsIO


def test_datasets_io(train_dataset, test_dataset):
    dg = TTVSets(name="TestContainer", train=train_dataset, test=test_dataset)

    TTVSetsIO.save(TTVSetsFormatsContainer.NpzFormat(), ".", dg)
    load_dg = TTVSetsIO.load("./TestContainer", TTVSetsFormatsContainer)

    for dataset, loaded_dataset in zip(
        [dg.train, dg.test], [load_dg.train, load_dg.test],
    ):
        x, y = dataset.items()
        xl, ly = loaded_dataset.items()

        assert x.tolist() == xl.tolist()

    assert load_dg.validation is None
