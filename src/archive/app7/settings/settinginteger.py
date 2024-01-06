from settings.setting import Setting


class SettingInteger(Setting):
    WIDGETTYPESPINBOX = 'spinbox'
    WIDGETTYPESLIDER = 'slider'
    WIDGETTYPES = [WIDGETTYPESPINBOX, WIDGETTYPESLIDER]

    def __init__(self, name: str, displayName: str, optional: bool=False, visible=True, minimum: int=0, maximum: int=100, step: int=1, defaultValue: int=0) -> None:
        super(SettingInteger, self).__init__(name=name, displayName=displayName, optional=optional, visible=visible)
        self._minimum = minimum
        self._maximum = maximum
        self._step = step
        self._defaultValue = defaultValue
        if self._defaultValue > self._maximum:
            self._maximum = self._defaultValue
        if self._defaultValue < self._minimum:
            self._minimum = self._defaultValue
        self._widgetType = SettingInteger.WIDGETTYPES[0]
        self.setValue(self._defaultValue)

    def minimum(self) -> int:
        return self._minimum

    def maximum(self) -> int:
        return self._maximum
    
    def step(self) -> int:
        return self._step
    
    def defaultValue(self) -> int:
        return self._defaultValue
    
    def isWidgetTypeSpinBox(self) -> bool:
        return self._widgetType == SettingInteger.WIDGETTYPES[0]
    
    def setWidgetTypeSpinBox(self) -> None:
        self._widgetType = SettingInteger.WIDGETTYPES[0]

    def isWidgetTypeSlider(self) -> bool:
        return self._widgetType == SettingInteger.WIDGETTYPES[1]
    
    def setWidgetTypeSlider(self) -> None:
        self._widgetType = SettingInteger.WIDGETTYPES[1]