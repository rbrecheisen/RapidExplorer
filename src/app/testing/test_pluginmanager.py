import pytest

from plugins.pluginmanager import PluginManager
from plugins.taskplugin import TaskPlugin

PLUGINDIR = 'src/app/plugins/plugins'


@pytest.mark.plugin
def test_loadTaskPlugins():
    manager = PluginManager()
    assert manager
    plugins = manager.loadTaskPlugins(PLUGINDIR, TaskPlugin)
    for pluginName in plugins['tasks'].keys():
        print(pluginName)