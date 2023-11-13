from plugins.taskplugin import TaskPlugin

PLUGINNAME = 'Delete DICOM File Task'


class DeleteDicomFileTaskPlugin(TaskPlugin):
    def __init__(self) -> None:
        super(DeleteDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return PLUGINNAME