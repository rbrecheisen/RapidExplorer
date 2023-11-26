from plugins.tasks.tasksetting import TaskSetting
from data.registeredfilesetmodel import RegisteredFileSetModel


class TaskFileSetSetting(TaskSetting):
    def __init__(self, name: str, value: RegisteredFileSetModel) -> None:
        super(TaskFileSetSetting, self).__init__(name=name, value=value)