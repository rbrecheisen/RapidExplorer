from PySide6.QtWidgets import QProgressBar

from tasks.taskwidget import TaskWidget
from tasks.createarchivetask.createarchivetask import CreateArchiveTask


class CreateArchiveTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CreateArchiveTaskWidget, self).__init__(taskType=CreateArchiveTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Creates ZIP Archive From File Set'
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