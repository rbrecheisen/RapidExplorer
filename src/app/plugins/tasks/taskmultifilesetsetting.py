from plugins.tasks.tasksetting import TaskSetting
from data.registeredmultifilesetmodel import RegisteredMultiFileSetModel


class TaskMultiFileSetSetting(TaskSetting):
    def __init__(self, name: str, value: RegisteredMultiFileSetModel) -> None:
        super(TaskFileSetSetting, self).__init__(name=name, value=value)