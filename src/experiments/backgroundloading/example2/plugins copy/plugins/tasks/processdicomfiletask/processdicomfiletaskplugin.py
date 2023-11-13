from plugins.taskplugin import TaskPlugin

PLUGINNAME = 'Process DICOM File Task'


class ProcessDicomFileTaskPlugin(TaskPlugin):
    def __init__(self):
        super(ProcessDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return PLUGINNAME