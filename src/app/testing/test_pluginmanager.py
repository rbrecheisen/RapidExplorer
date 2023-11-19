import pytest

from plugins.pluginmanager import PluginManager
from plugins.taskplugin import TaskPlugin

PLUGINDIR = 'src/experiments/backgroundloading/example2/plugins'


@pytest.mark.plugins
def test_loadTaskPlugins():
    manager = PluginManager()
    assert manager
    plugins = manager.loadTaskPlugins(PLUGINDIR, TaskPlugin)
    for pluginName in plugins['tasks'].keys():
        print(pluginName)