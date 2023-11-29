from typing import Dict

from PySide6.QtCore import QRunnable

from tasks.tasksignal import TaskSignal
from data.fileset import FileSet


class Task(QRunnable):
    def __init__(self, name: str) -> None:
        super(Task, self).__init__()
        self._name = name
        self._inputFileSets = {}
        self._outputFileSetDirectory = None
        self._outputFileSet = None
        self._nrSteps = 0
        self._signal = TaskSignal()

    def name(self) -> str:
        return self._name
    
    def inputFileSets(self) -> Dict[str, FileSet]:
        return self._inputFileSets
    
    def inputFileSet(self, name: str) -> FileSet:
        return self._inputFileSets[name]
    
    def addInputFileSet(self, fileSet: FileSet, name: str) -> None:
        self._inputFileSets[name] = fileSet

    def outputFileSetDirectory(self) -> str:
        return self._outputFileSetDirectory
    
    def setOutputFileSetDirectory(self, outputFileSetDirectory: str) -> None:
        self._outputFileSetDirectory = outputFileSetDirectory

    def outputFileSet(self) -> FileSet:
        return self._outputFileSet
    
    def setOutputFileSet(self, outputFileSet: FileSet) -> None:
        self._outputFileSet = outputFileSet

    def nrSteps(self) -> int:
        self._nrSteps

    def setNrSteps(self, nrSteps: int) -> None:
        self._nrSteps = nrSteps

    def signal(self) -> TaskSignal:
        return self._signal

    def run(self) -> None:
        raise NotImplementedError('Not implemented')