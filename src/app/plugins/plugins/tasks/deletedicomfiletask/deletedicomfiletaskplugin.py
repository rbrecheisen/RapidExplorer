from plugins.taskplugin import TaskPlugin

PLUGINNAME = 'DeleteDicomFileTaskPlugin'


class DeleteDicomFileTaskPlugin(TaskPlugin):
    def __init__(self) -> None:
        super(DeleteDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return PLUGINNAME