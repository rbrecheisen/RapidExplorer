from settings.setting import Setting


class SettingInteger(Setting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True, minimum: int=0, maximum: int=100, defaultValue: int=0) -> None:
        super(SettingInteger, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._minimum = minimum
        self._maximum = maximum
        self._defaultValue = defaultValue
        self.setValue(self._defaultValue)

    def minimum(self) -> int:
        return self._minimum

    def maximum(self) -> int:
        return self._maximum
    
    def defaultValue(self) -> int:
        return self._defaultValue