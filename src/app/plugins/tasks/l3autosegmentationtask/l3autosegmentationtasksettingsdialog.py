from plugins.tasks.tasksettingsdialog import TaskSettingsDialog


class L3AutoSegmentationTaskSettingsDialog(TaskSettingsDialog):
    def __init__(self, task) -> None:
        super(L3AutoSegmentationTaskSettingsDialog, self).__init__(task=task)