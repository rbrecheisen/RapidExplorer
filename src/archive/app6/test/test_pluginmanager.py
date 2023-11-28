import pytest

from plugins.pluginmanager import PluginManager


@pytest.mark.plugin
def test_loadTaskPlugins():
    manager = PluginManager()
    assert manager
    plugins = manager.loadTaskPlugins()
    for pluginName in plugins['tasks'].keys():
        print(pluginName)