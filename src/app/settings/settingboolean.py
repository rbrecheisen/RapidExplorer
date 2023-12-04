from settings.setting import Setting


class SettingBoolean(Setting):
    def __init__(self, name: str, displayName: str, optional: bool=False, visible: bool=True, defaultValue: bool=True) -> None:
        super(SettingBoolean, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._defaultValue = defaultValue
        self.setValue(self._defaultValue)

    def defaultValue(self) -> bool:
        return self._defaultValue