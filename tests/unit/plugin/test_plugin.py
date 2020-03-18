# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_plugin_creation(plugin):
    assert plugin.name == "test-plugin"
    assert plugin.version == "0.1.2"
    assert plugin.summary == "A Test Plugin."
    assert plugin.active is True


def test_plugin_load(plugin):
    plugin.load()

    assert plugin.active is True


def test_plugin_unload(plugin):
    plugin.unload()

    assert plugin.active is False


# def test_reload_plugin(plugin):
#     plugin.load()
#     plugin.unload()
#     plugin.load()
