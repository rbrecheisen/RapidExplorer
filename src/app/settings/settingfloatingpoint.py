from settings.setting import Setting


class SettingFloatingPoint(Setting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True, minimum: float=0, maximum: float=100, defaultValue: float=0) -> None:
        super(SettingFloatingPoint, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._minimum = minimum
        self._maximum = maximum
        self._defaultValue = defaultValue
        self.setValue(self._defaultValue)

    def minimum(self) -> float:
        return self._minimum

    def maximum(self) -> float:
        return self._maximum
    
    def defaultValue(self) -> float:
        return self._defaultValue