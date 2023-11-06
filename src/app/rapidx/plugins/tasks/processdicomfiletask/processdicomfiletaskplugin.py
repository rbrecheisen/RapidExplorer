from rapidx.app.plugins.taskplugin import TaskPlugin


class ProcessDicomFileTaskPlugin(TaskPlugin):
    def __init__(self):
        super(ProcessDicomFileTaskPlugin, self).__init__()

    def name(self) -> str:
        return 'ProcessDicomFileTaskPlugin'