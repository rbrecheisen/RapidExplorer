class Task:
    IDLE = 0
    START = 1
    RUNNING = 2
    CANCELLING = 3
    CANCELED = 4
    FINISHED = 5
    ERROR = 6

    def __init__(self, name: str) -> None:
        self._name = name
        self._status = Task.IDLE

    def name(self) -> str:
        return self._name
    
    def status(self) -> int:
        return self._status
    
    def setStatus(self, status: int) -> None:
        self._status = status

    def start(self) -> None:
        raise NotImplementedError()
    
    def cancel(self) -> None:
        raise NotImplementedError()