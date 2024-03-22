from PySide6.QtWidgets import QProgressBar

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.calculatebodycompositionmetricstask.calculatebodycompositionmetricstask import CalculateBodyCompositionMetricsTaskTask


class CalculateBodyCompositionMetricsTaskWidget(TaskWidget):
    def __init__(self, progressBar: QProgressBar) -> None:
        super(CalculateBodyCompositionMetricsTaskWidget, self).__init__(taskType=CalculateBodyCompositionMetricsTaskTask, progressBar=progressBar)
    
    def validate(self) -> None:
        pass