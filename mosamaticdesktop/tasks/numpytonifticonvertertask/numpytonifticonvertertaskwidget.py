from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.numpytonifticonvertertask.numpytonifticonvertertask import NumPyToNiftiConverterTask


class NumPyToNiftiConverterTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(NumPyToNiftiConverterTaskWidget, self).__init__(taskType=NumPyToNiftiConverterTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Converts 2D or 3D NumPy arrays to NIFTI format'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input File Set Name',
        )
        self.addTextParameter(
            name='transformationMatrix',
            labelText='Affine Transformation Matrix',
            optional=True,
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