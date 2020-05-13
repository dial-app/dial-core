# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import tensorflow as tf

# from dial_core.datasets import Dataset, datatype


class DataAugmentator:
    def __init__(self):
        self.target_shape = (500, 500)

        def resize(data):
            return self.fun(data)

        self.pfun = resize

    def fun(self, data):
        image = tf.keras.preprocessing.image.array_to_img(data)

        image = image.resize(self.target_shape)

        return tf.keras.preprocessing.image.img_to_array(image)


# def test_ttv_io():
#     pass
#     ttv_sets = FashionMnistLoader().load()

#     dataset_desc = (
#         CategoricalImgDatasetIO().set_organization(
#             CategoricalImgDatasetIO.Organization.CategoryOnFolders
#         )
#         # .set_filename_category_regex(r"^(\d+)")
#         .save_to_file("TestContainer/fashion/description.json", ttv_sets.test)
#     )

#     print(dataset_desc)

#     dataset = (
#         CategoricalImgDatasetIO()
#         .set_organization(CategoricalImgDatasetIO.Organization.CategoryOnFolders)
#         .set_filename_category_regex("(.*?)__")
#         .load_from_file("/home/david/dial-core/TestContainer/fashion/description.json")
#     )

#     print("Y", dataset.y)

#     pytest.fail("ASDF")

# dataset = CategoricalImgDatasetIO().load_from_file(
#     "TestContainer/mnist/description.json"
# )

# print(dataset.x)
# print(dataset.y)

# ttv = TTVSetsIO.load("TestContainer/MNIST")

# print(ttv.train.y)

# ttv_sets = TTVSetsIO.load(
#     "/home/david/dial-gui/projects/Default Project/Fashion MNIST"
# )

# print(ttv_sets.train.items(role=Dataset.Role.Display))

# pytest.fail("asdf")
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
