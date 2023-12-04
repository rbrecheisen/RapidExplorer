from settings.settingtext import SettingText


class SettingFileSetPath(SettingText):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True) -> None:
        super(SettingFileSetPath, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)