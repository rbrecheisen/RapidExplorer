from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.calculatebodycompositionmetricstask.calculatebodycompositionmetricstask import CalculateBodyCompositionMetricsTaskTask


class CalculateBodyCompositionMetricsTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CalculateBodyCompositionMetricsTaskWidget, self).__init__(taskType=CalculateBodyCompositionMetricsTaskTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Calculates body composition metrics on predicted segmenations and TAG files if available'
        )
        self.addFileSetParameter(
            name='inputFileSetName',
            labelText='Input DICOM (and TAG) File Set',
        )
        self.addFileSetParameter(
            name='inputSegmentationFileSetName',
            labelText='Input Segmentation File Set',
        )
        self.addPathParameter(
            name='patientHeightsCsvFilePath',
            labelText='Patient Height CSV File Path (File Name, Height (m))',
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