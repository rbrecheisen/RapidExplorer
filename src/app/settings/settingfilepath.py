from settings.settingtext import SettingText


class SettingFilePath(SettingText):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True) -> None:
        super(SettingFilePath, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)