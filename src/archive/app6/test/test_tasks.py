import pytest

"""
What do I need for tasks? I need a list of tasks to show in a combobox (like in Mosamatic). 
Also, I need a table showing the current task instances (different class?) with their
properties like start time, status, datasets it operates on, refresh/cancel/delete buttons.
From this information I need tests for the following:

 - Create new task instance from task definition
 - Start task instance with properties defined by task definition
 - Delete task instance

 Classes:

 - TaskDefinition
 - TaskInstance
"""

@pytest.mark.task
def test_listTaskDefinitions():
    pass

def test_createNewTaskInstance():
    pass
