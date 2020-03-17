# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_plugin_creation(plugin):
    assert plugin.name == "test-plugin"
    assert plugin.version == "0.1.2"
    assert plugin.description == "A Test Plugin."
    assert plugin.path == "test-plugin"
    assert not plugin.active
    assert not plugin.loaded


def test_plugin_load(plugin):
    plugin.load()

    assert plugin.loaded is True
    assert plugin.active is True


def test_plugin_unload(plugin):
    plugin.unload()

    assert plugin.loaded is False
    assert plugin.active is False


# def test_reload_plugin(plugin):
#     plugin.load()
#     plugin.unload()
#     plugin.load()
