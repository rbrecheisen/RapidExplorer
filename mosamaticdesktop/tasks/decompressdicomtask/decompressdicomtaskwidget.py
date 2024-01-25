from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.decompressdicomtask.decompressdicomtask import DecompressDicomTask


class DecompressDicomTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(DecompressDicomTaskWidget, self).__init__(taskType=DecompressDicomTask, progressBar=progressBar)
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