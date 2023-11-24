class Task:
    def __init__(self, name: str) -> None:
        self._name = name
        self._data = {}
        self._parameters = {}

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
    
    def addParameter(self, name: str, value) -> None:
        if name in self._parameters.keys():
            raise RuntimeError(f'Parameter with name {name} already added to task')
        self._parameters[name] = value

    def hasParameter(self, name) -> bool:
        return name in self._parameters.keys()
    
    def parameter(self, name: str):
        return self._parameters[name]

    def execute(self) -> None:
        raise NotImplementedError('Not implemented')
    
    def outputData(self):
        raise NotImplementedError('Not implemented')