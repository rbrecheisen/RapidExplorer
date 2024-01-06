from settings.setting import Setting


class SettingText(Setting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True, maximumLength: int=1024, defaultValue='') -> None:
        super(SettingText, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._maximumLength = maximumLength
        self._defaultValue = defaultValue
        self.setValue(self._defaultValue)

    def maximumLength(self) -> int:
        return self._maximumLength
    
    def defaultValue(self) -> str:
        return self._defaultValue