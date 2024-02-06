from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromsegmentationfiletask.createpngfromsegmentationfiletask import CreatePngFromSegmentationFileTask


class CreatePngFromSegmentationFileTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreatePngFromSegmentationFileTaskWidget, self).__init__(taskType=CreatePngFromSegmentationFileTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description=f'Create PNGs From NumPy Files',
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
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