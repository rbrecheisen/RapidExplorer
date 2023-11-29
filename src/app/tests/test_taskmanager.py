from tasks.taskmanager import TaskManager
from tasks.task import Task


def test_taskManagerCanFindTasks():
    manager = TaskManager()
    manager.loadTasks()
    assert len(manager.tasks()) > 0


def test_taskManagerCanInitializeTask():
    pass


def test_taskManagerCanStartTask():
    pass


