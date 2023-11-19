import pytest

from rapidx.app.plugins.pluginmanager import PluginManager
from rapidx.app.plugins.taskplugin import TaskPlugin

PLUGINDIR = 'src/app/rapidx/plugins'


@pytest.mark.plugins
def test_loadTaskPlugins():
    manager = PluginManager()
    assert manager
    plugins = manager.loadTaskPlugins(PLUGINDIR, TaskPlugin)
    for pluginName in plugins['tasks'].keys():
        print(pluginName)