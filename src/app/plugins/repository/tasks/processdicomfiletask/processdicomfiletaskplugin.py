from plugins.taskplugin import TaskPlugin

PLUGINNAME = 'ProcessDicomFileTaskPlugin'


class ProcessDicomFileTaskPlugin(TaskPlugin):
    def __init__(self):
        super(ProcessDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return PLUGINNAME