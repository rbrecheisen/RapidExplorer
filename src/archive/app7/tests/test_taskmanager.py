from tasks.taskmanager import TaskManager


def test_taskManagerCanFindTasks():
    manager = TaskManager()
    manager.loadTaskTypes()
    assert len(manager.taskTypes()) > 0


def test_taskManagerCanInitializeTask():
    pass


def test_taskManagerCanStartTask():
    pass


