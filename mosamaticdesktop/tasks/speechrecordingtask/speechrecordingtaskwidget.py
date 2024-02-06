from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.speechrecordingtask.speechrecordingtask import SpeechRecordingTask


class SpeechRecordingTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(SpeechRecordingTaskWidget, self).__init__(taskType=SpeechRecordingTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Records audio and saves it to .wav file',
        )
        self.addPathParameter(
            name='outputFileSetPath',
            labelText='Output File Set Path',
        )
        self.addTextParameter(
            name='outputFileSetName',
            labelText='Output File Set Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputFileSet',
            labelText='Overwrite Output File Set',
            defaultValue=True,
        )
    
    def validate(self) -> None:
        pass        