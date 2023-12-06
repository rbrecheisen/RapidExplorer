from settings.setting import Setting


class SettingLabel(Setting):
    def __init__(self, name: str, value: str) -> None:
        super(SettingLabel, self).__init__(name=name, displayName='Info', optional=False, visible=True)
        self.setValue(value)