from barbell2_bodycomp import MuscleFatSegmentator, BodyCompositionCalculator
from barbell2_bodycomp.convert import npy2png, dcm2npy

from plugins.tasks.task import Task
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class L3AutoSegmentationTask(Task):
    def __init__(self) -> None:
        super(L3AutoSegmentationTask, self).__init__(name='L3 Auto-Segmentation')
        self._outputData = None

    def run(self) -> None:
        inputData = self.data(name='inputData')
        print(inputData)

    def outputData(self) -> RegisteredMultiFileSetModel:
        return self._outputData