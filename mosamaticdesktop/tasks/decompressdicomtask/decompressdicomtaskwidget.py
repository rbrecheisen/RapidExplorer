from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.decompressdicomtask.decompressdicomtask import DecompressDicomTask


class DecompressDicomTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DecompressDicomTaskWidget, self).__init__(taskType=DecompressDicomTask)

    def validate(self) -> None:
        pass