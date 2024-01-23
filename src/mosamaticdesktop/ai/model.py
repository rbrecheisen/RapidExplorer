import numpy as np


class Model:
    def __init__(self) -> None:
        self._model = None

    def load(self, modelFilePath: str) -> None:
        raise NotImplementedError()

    def predict(self, input: np.array) -> np.array:
        raise NotImplementedError()