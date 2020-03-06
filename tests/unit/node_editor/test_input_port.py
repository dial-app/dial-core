# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pickle


def test_port_connected_to(input_port_a, output_port_a):

    assert input_port_a.port_connected_to is None

    input_port_a.connect_to(output_port_a)

    assert input_port_a.port_connected_to is output_port_a


def test_input_port_attributes(input_port_a):
    assert hasattr(input_port_a, "name")
    assert hasattr(input_port_a, "port_type")


# TODO: Mock open call to avoid creating a file
def test_pickle_input_port(input_port_a):
    with open("input_port_a.pickle", "wb") as binary_file:
        pickle.dump(input_port_a, binary_file, protocol=pickle.HIGHEST_PROTOCOL)

    with open("input_port_a.pickle", "rb") as binary_file:
        loaded_input_port_a = pickle.load(binary_file)

        test_input_port_attributes(loaded_input_port_a)
