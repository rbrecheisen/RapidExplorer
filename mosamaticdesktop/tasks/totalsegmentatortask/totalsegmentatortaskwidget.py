from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatortask.totalsegmentatortask import TotalSegmentatorTask


class TotalSegmentatorTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(TotalSegmentatorTaskWidget, self).__init__(taskType=TotalSegmentatorTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Extracts anatomical ROIs from list of full CT scans'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory of CT Scans (Each Scan as Separate Sub-Directory)'
        )
        self.addPathParameter(
            name='outputDirectoryPath',
            labelText='Output Directory with Segmentations'
        )
        self.addTextParameter(
            name='outputDirectoryName',
            labelText='Output Directory Name',
            optional=True,
        )
        self.addBooleanParameter(
            name='overwriteOutputDirectory',
            labelText='Overwrite Output Directory',
            defaultValue=True,
        )
    
    def validate(self) -> None:
        pass