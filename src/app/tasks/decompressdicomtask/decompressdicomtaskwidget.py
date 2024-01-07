from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class DecompressDicomTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(DecompressDicomTaskWidget, self).__init__(taskType=DummyTask)
        self.addDescriptionParameter(
            name='description',
            description='Decompresses JPEG200-compressed DICOM files for use in Slice-o-matic.'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set Name',
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
    
    def validate(self) -> None:
        pass