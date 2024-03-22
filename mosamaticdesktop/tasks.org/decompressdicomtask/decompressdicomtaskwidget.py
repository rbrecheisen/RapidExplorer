from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.decompressdicomtask.decompressdicomtask import DecompressDicomTask


class DecompressDicomTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(DecompressDicomTaskWidget, self).__init__(taskType=DecompressDicomTask, progressBar=progressBar)

    def validate(self) -> None:
        pass