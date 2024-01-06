from settings.setting import Setting


class SettingFileSet(Setting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True) -> None:
        super(SettingFileSet, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)