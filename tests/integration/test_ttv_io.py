# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from dial_core.datasets.io import NpzDatasetIO, TTVSetsIO


def test_ttv_io(ttv_sets):
    TTVSetsIO.save("TestContainer", NpzDatasetIO, ttv_sets)
    ttv_sets = TTVSetsIO.load("TestContainer/TTVSets")

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
