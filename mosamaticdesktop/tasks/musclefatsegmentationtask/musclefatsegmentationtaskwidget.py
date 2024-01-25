from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.musclefatsegmentationtask.musclefatsegmentationtask import MuscleFatSegmentationTask


class MuscleFatSegmentationTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(MuscleFatSegmentationTaskWidget, self).__init__(taskType=MuscleFatSegmentationTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Extract muscle and fat regions from L3 images'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
        )
        self.addFileSetParameter(
            name='tensorFlowModelFileSetName',
            labelText='TensorFlow Model File Set',
        )
        self.addOptionGroupParameter(
            name='mode',
            labelText='Mode',
            defaultValue='ARGMAX',
            options=['ARGMAX', 'PROBABILITIES'],
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