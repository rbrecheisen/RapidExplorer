from rapidx.app.plugins.pluginmanager import PluginManager


def test_loadAllPlugins():
    manager = PluginManager()
    assert manager