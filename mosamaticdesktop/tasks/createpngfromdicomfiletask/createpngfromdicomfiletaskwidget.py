from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.createpngfromdicomfiletask.createpngfromdicomfiletask import CreatePngFromDicomFileTask


class CreatePngFromDicomFileTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreatePngFromDicomFileTaskWidget, self).__init__(taskType=CreatePngFromDicomFileTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description=f'Create PNGs From DICOM Files',
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set',
        )
        self.addIntegerParameter(
            name='windowLevel',
            labelText='Window Level',
            minimum=0,
            maximum=2000,
            step=1,
            defaultValue=50,
        )
        self.addIntegerParameter(
            name='windowWidth',
            labelText='Window Width',
            minimum=0,
            maximum=2000,
            step=1,
            defaultValue=400,
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