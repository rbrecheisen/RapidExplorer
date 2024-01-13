from tasks.taskwidget import TaskWidget
from tasks.copyfilesettask.copyfilesettask import CopyFileSetTask


class CopyFileSetTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CopyFileSetTaskWidget, self).__init__(taskType=CopyFileSetTask)
        self.addDescriptionParameter(
            name='description',
            description='Copies one or more filesets to another fileset'
        )
    
    def validate(self) -> None:
        pass