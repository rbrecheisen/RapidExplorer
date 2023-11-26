from plugins.tasks.tasksetting import TaskSetting
from data.registeredfilemodel import RegisteredFileModel


class TaskFileSetting(TaskSetting):
    def __init__(self, name: str, value: RegisteredFileModel) -> None:
        super(TaskFloatingPointSetting, self).__init__(name=name, value=value)