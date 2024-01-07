from tasks.taskwidget import TaskWidget
from tasks.dummytask.dummytask import DummyTask


class CheckDicomHeaderTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CheckDicomHeaderTaskWidget, self).__init__(taskType=DummyTask)
        self.addLabelParameter(
            name='description',
            labelText='Check DICOM headers XXXXXX XXXXXX XXXXXXXXX XXXXXXXXX XXXXXXXXXX XXXXXXXXX',
            optional=False,
            visible=True,
            defaultValue=None,
        )