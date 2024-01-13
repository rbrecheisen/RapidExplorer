from tasks.taskwidget import TaskWidget
from tasks.createpngtask.createpngtask import CreatePngTask

SUPPORTEDFILETYPES = [
    'DICOM',
    'NumPy',
    'TAG',
]


class CreatePngTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CreatePngTaskWidget, self).__init__(taskType=CreatePngTask)
        fileTypes = ''
        nr = len(SUPPORTEDFILETYPES)
        for i in range(nr):
            if i < nr - 1:
                fileTypes += SUPPORTEDFILETYPES[i] + ', '
            else:
                fileTypes += ' and ' + SUPPORTEDFILETYPES[i]
        self.addDescriptionParameter(
            name='description',
            description=f'Create PNGs From {fileTypes} Files',
        )
    
    def validate(self) -> None:
        pass