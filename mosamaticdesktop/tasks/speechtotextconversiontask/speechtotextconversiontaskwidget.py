from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.speechtotextconversiontask.speechtotextconversiontask import SpeechToTextConversionTask


class SpeechToTextConversionTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(SpeechToTextConversionTaskWidget, self).__init__(taskType=SpeechToTextConversionTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Loads audio file (MP3) and converts it to text using Coqui-TTS package',
        )
        self.addFilePathParameter(
            name='inputFilePath',
            labelText='Input File Path to WAV Audio File',
        )
        self.addOptionGroupParameter(
            name='modelName',
            labelText='Model Name',
            options=['base', 'medium', 'large'],
            defaultValue='large',
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