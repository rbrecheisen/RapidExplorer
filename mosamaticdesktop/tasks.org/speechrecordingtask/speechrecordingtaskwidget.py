from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.speechrecordingtask.speechrecordingtask import SpeechRecordingTask


class SpeechRecordingTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(SpeechRecordingTaskWidget, self).__init__(taskType=SpeechRecordingTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass        