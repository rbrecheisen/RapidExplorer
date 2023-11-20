from plugins.task import Task


class TaskPlugin:
    def __init__(self, name: str=None, task: Task=None) -> None:
        self._name = name
        self._task = task

    def name(self) -> str:
        return self._name
    
    def implementation(self) -> Task:
        return self._task