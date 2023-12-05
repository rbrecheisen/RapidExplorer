from tasks.task import Task
from tasks.tasksignal import TaskSignal


class CreateArchiveTask(Task):
    NAME = 'CreateArchiveTask'

    def __init__(self) -> None:
        super(CreateArchiveTask, self).__init__()