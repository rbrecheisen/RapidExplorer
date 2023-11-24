from plugins.taskplugin import TaskPlugin
from plugins.tasks.copyfilesettask.copyfilesettask import CopyFileSetTask

PLUGINNAME = 'CopyFileSetTaskPlugin'


class CopyFileSetTaskPlugin(TaskPlugin):
    def __init__(self):
        super(CopyFileSetTaskPlugin, self).__init__(name=PLUGINNAME, task=CopyFileSetTask())