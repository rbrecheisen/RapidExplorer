from rapidx.app.plugins.taskplugin import TaskPlugin


class DeleteDicomFileTaskPlugin(TaskPlugin):
    def __init__(self):
        super(DeleteDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return 'DeleteDicomFileTaskPlugin'