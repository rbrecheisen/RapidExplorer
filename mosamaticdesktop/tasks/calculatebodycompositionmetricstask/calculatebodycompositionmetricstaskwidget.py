from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.calculatebodycompositionmetricstask.calculatebodycompositionmetricstask import CalculateBodyCompositionMetricsTaskTask


class CalculateBodyCompositionMetricsTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CalculateBodyCompositionMetricsTaskWidget, self).__init__(taskType=CalculateBodyCompositionMetricsTaskTask)
    
    def validate(self) -> None:
        pass