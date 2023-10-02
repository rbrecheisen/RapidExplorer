from com.application.tab import Tab


class ViewTab(Tab):

    TITLE = 'View'
    EMPTY_TEXT = 'This is the Views tab'

    def __init__(self) -> None:
        super(ViewTab, self).__init__()
