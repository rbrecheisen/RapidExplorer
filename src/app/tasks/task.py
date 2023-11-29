from PySide6.QtCore import QRunnable


class Task(QRunnable):
    def __init__(self, name: str) -> None:
        super(Task, self).__init__()
        self._name = name

    def name(self) -> str:
        return self._name

    def run(self) -> None:
        raise NotImplementedError('Not implemented')