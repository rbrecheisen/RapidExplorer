from plugins.taskplugin import TaskPlugin

PLUGINNAME = 'GenerateFileSetTaskPlugin'


class GenerateFileSetTaskPlugin(TaskPlugin):
    def __init__(self):
        super(GenerateFileSetTaskPlugin, self).__init__()

    def name(self) -> str:
        return PLUGINNAME
