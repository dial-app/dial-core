# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# import pytest

# from dial_core.datasets.io import (
#     CategoricalImgDatasetIO,
#     MnistLoader,
#     NpzDatasetIO,
#     TTVSetsIO,
# )


def test_ttv_io():
    pass
    # ttv_sets = MnistLoader().load()

    # TTVSetsIO.save("TestContainer", CategoricalImgDatasetIO, ttv_sets)

    # ttv = TTVSetsIO.load("TestContainer/MNIST")

    # print(ttv.train.y)

    # ttv_sets = TTVSetsIO.load("TestContainer/TTVSets")

    # NpzDatasetIO.save("train", "foo/description.json", ttv_sets.train)
    # TTVSetsIO.save("foo", NpzDatasetIO, ttv_sets)

    # dg = TTVSets(name="TestContainer", train=train_dataset, test=test_dataset)

    # TTVSetsIO.save(TTVSetsFormatsContainer.NpzFormat(), ".", dg)
    # load_dg = TTVSetsIO.load("./TestContainer", TTVSetsFormatsContainer)

    # for dataset, loaded_dataset in zip(
    #     [dg.train, dg.test], [load_dg.train, load_dg.test],
    # ):
    #     x, y = dataset.items()
    #     xl, ly = loaded_dataset.items()

    #     assert x.tolist() == xl.tolist()

    # assert load_dg.validation is None
