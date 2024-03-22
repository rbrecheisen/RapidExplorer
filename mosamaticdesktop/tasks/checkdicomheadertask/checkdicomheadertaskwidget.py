from pydicom.datadict import keyword_dict

from mosamaticdesktop.tasks.taskwidget import TaskWidget
from mosamaticdesktop.tasks.checkdicomheadertask.checkdicomheadertask import CheckDicomHeaderTask


class CheckDicomHeaderTaskWidget(TaskWidget):
    def __init__(self) -> None:
        super(CheckDicomHeaderTaskWidget, self).__init__(taskType=CheckDicomHeaderTask)

    def validate(self) -> None:
        requiredAttributes = self.taskParameterWidget('requiredAttributes').parameter().value()
        if requiredAttributes != '':
            attributes = [x.strip() for x in requiredAttributes.split(',')]
            for attribute in attributes:
                if attribute not in keyword_dict:
                    self.showValidationError('requiredAttributes', f'Attribute {attribute} is not a valid DICOM attribute')
                    return