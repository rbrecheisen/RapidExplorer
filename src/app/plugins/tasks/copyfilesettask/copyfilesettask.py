from plugins.task import Task

TASKNAME = 'Copy File Set'


class CopyFileSetTask(Task):
    def __init__(self) -> None:
        super(CopyFileSetTask, self).__init__(name=TASKNAME)