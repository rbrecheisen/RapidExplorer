import threading


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
        self._progress = 0
        self._thread = None

    def name(self) -> str:
        return self._name
    
    def status(self) -> int:
        return self._status
    
    def setStatus(self, status: int) -> None:
        self._status = status

    def progress(self) -> int:
        return self._progress

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run)
        self._thread.start()

    def run(self) -> None:
        raise NotImplementedError()
    
    def cancel(self) -> None:
        self.setStatus(status=Task.CANCELLING)
        self._thread.join()