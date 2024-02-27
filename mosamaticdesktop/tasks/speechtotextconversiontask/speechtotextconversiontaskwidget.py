from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.speechtotextconversiontask.speechtotextconversiontask import SpeechToTextConversionTask


class SpeechToTextConversionTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(SpeechToTextConversionTaskWidget, self).__init__(taskType=SpeechToTextConversionTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass        