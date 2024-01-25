from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.copyfilesettask.copyfilesettask import CopyFileSetTask


class CopyFileSetTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CopyFileSetTaskWidget, self).__init__(taskType=CopyFileSetTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Copies one or more filesets to another fileset'
        )
        self.addMultiFileSetParameter(
            name='inputFileSetNames',
            labelText='Input File Set Names',
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