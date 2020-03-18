# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


def test_installed_plugins(plugin_manager):
    assert len(plugin_manager.installed_plugins) == 1

    assert plugin_manager.installed_plugins["test-plugin"] is not None


# def test_install_inexistent_plugin(plugin_manager):
#     with pytest.raises(FileNotFoundError):
#         plugin_manager.install_plugin("foo-bar-foo")


def test_load_plugin(plugin_manager):
    plugin_manager.load_plugin("test-plugin")
    assert plugin_manager.installed_plugins["test-plugin"].active is True
