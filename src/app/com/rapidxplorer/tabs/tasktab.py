from com.rapidxplorer.tabs.tab import Tab


class TaskTab(Tab):

    TITLE = 'Task'
    EMPTY_TEXT = 'This is the Tasks tab'

    def __init__(self) -> None:
        super(TaskTab, self).__init__()
