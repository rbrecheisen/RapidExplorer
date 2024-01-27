from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.totalsegmentatorsliceselectiontask.totalsegmentatorsliceselectiontask import TotalSegmentatorSliceSelectionTask

ROIS = [
    'vertebrae_S1', 'vertebrae_C1', 'vertebrae_C2', 'vertebrae_C3', 'vertebrae_C4', 'vertebrae_C5', 'vertebrae_C6', 'vertebrae_C7', 
    'vertebrae_L1', 'vertebrae_L2', 'vertebrae_L3', 'vertebrae_L4', 'vertebrae_L5', 'vertebrae_T1', 'vertebrae_T2', 'vertebrae_T3', 
    'vertebrae_T4', 'vertebrae_T5', 'vertebrae_T6', 'vertebrae_T7', 'vertebrae_T8', 'vertebrae_T9', 'vertebrae_T10', 'vertebrae_T11', 
    'vertebrae_T12'
]


class TotalSegmentatorSliceSelectionTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(TotalSegmentatorSliceSelectionTaskWidget, self).__init__(taskType=TotalSegmentatorSliceSelectionTask, progressBar=progressBar)
        self.addDescriptionParameter(
            name='description',
            description='Extracts vertebral images from CT scans'
        )
        self.addPathParameter(
            name='rootDirectoryPath',
            labelText='Root Directory of CT Scans (Each Scan as Separate Sub-Directory)'
        )
        self.addOptionGroupParameter(
            name='vertebra',
            labelText='Vertebral ROI From TotalSegmentator Output',
            options=ROIS,
        )
        self.addPathParameter(
            name='outputDirectoryPath',
            labelText='Output Directory with Selected Images'
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