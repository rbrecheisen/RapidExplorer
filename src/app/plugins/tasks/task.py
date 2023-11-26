class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        self._data = {}
        self._settings = {}

    def name(self) -> str:
        return self._name
    
    def addData(self, data, name: str) -> None:
        if name in self._data.keys():
            raise RuntimeError(f'Data with name {name} already added to task')
        self._data[name] = data

    def hasData(self, name: str) -> bool:
        return name in self._data.keys()

    def data(self, name: str):
        return self._data[name]
    
    def addSetting(self, name: str, value) -> None:
        if name in self._settings.keys():
            raise RuntimeError(f'Setting with name {name} already added to task')
        self._settings[name] = value

    def hasSetting(self, name) -> bool:
        return name in self._settings.keys()
    
    def setting(self, name: str):
        return self._settings[name]
    
    def showSettingsDialog(self) -> None:
        raise NotImplementedError('Not implemented')

    def run(self) -> None:
        # To be run in the background using QThreadPool
        raise NotImplementedError('Not implemented')
    
    def outputData(self):
        raise NotImplementedError('Not implemented')