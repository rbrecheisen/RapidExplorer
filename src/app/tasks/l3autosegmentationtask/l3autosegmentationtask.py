# from barbell2_bodycomp import MuscleFatSegmentator, BodyCompositionCalculator

from tasks.task import Task
from data.fileset import FileSet


class L3AutoSegmentationTask(Task):
    def __init__(self) -> None:
        super(L3AutoSegmentationTask, self).__init__(name='L3AutoSegmentationTask')
        self._inputFileSets = {}
        self._outputDirectory = None

    def outputDirectory(self) -> str:
        # Move to Task class
        return self._outputDirectory

    def setOutputDirectory(self, outputDirectory: str) -> None:
        # Move to Task class
        self._outputDirectory = outputDirectory

    def addInputFileSet(self, fileSet: FileSet, name: str) -> None:
        # Move to Task class
        self._inputFileSets[name] = fileSet

    def getInputFileSet(self, name: str) -> FileSet:
        return self._inputFileSets[name]

    def run(self) -> None:
        pass