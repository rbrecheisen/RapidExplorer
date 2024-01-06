import threading

from typing import Dict

from tasks.parameter import Parameter


class Task:
    IDLE = 0
    START = 1
    RUNNING = 2
    CANCELING = 3
    CANCELED = 4
    FINISHED = 5
    ERROR = 6

    @classmethod
    def NAME(cls):
        # Returns class name of child classes
        return cls.__qualname__

    def __init__(self) -> None:
        self._status = Task.IDLE
        self._progress = 0
        self._thread = None
        self._errors = []
        self._parameters = None

    def name(self) -> str:
        return self.__class__.__name__
    
    def setParameters(self, parameters: Dict[str, Parameter]) -> None:
        self._parameters = parameters
    
    def parameter(self, name: str) -> Parameter:
        if name in self._parameters.keys():
            return self._parameters[name]
        return None
    
    def errors(self) -> List[str]:
        return self._errors
    
    def addError(self, message: str) -> None:
        self._errors.append(message)

    def hasErrors(self) -> bool:
        return len(self._errors) > 0
    
    # Status
    
    def status(self) -> int:
        return self._status
    
    def statusIsIdle(self) -> bool:
        return self._status == Task.IDLE
    
    def statusIsStart(self) -> bool:
        return self._status == Task.START
    
    def statusIsRunning(self) -> bool:
        return self._status == Task.RUNNING
    
    def statusIsCanceling(self) -> bool:
        return self._status == Task.CANCELING
    
    def statusIsCanceled(self) -> bool:
        return self._status == Task.CANCELED
    
    def statusIsFinished(self) -> bool:
        return self._status == Task.FINISHED
    
    def statusIsError(self) -> bool:
        return self._status == Task.ERROR
    
    def setStatus(self, status: int) -> None:
        self._status = status

    def setStatusIdle(self) -> None:
        self._status = Task.IDLE

    def setStatusStart(self) -> None:
        self._status = Task.START

    def setStatusRunning(self) -> None:
        self._status = Task.RUNNING

    def setStatusCanceling(self) -> None:
        self._status = Task.CANCELING

    def setStatusCanceled(self) -> None:
        self._status = Task.CANCELED

    def setStatusFinished(self) -> None:
        self._status = Task.FINISHED

    def setStatusError(self) -> None:
        self._status = Task.ERROR

    # Progress

    def progress(self) -> int:
        return self._progress
    
    def setProgress(self, step: int, nrSteps: int) -> None:
        self._progress = int(((step + 1) / (nrSteps)) * 100)

    # Execution

    def start(self) -> None:
        self.setStatusStart()
        self._thread = threading.Thread(target=self.run)
        self._thread.start()
        self.setStatusRunning()

    def run(self) -> None:
        raise NotImplementedError()
    
    def cancel(self) -> None:
        self.setStatusCanceling()
        self._thread.join()