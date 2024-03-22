import numpy as np

from mosamaticdesktop.tasks.musclefatsegmentationtask.model import Model


class PyTorchModel(Model):
    def __init__(self) -> None:
        super(PyTorchModel, self).__init__()
        self._model = None

    def load(self, modelFilePath: str) -> None:
        pass

    def predict(self, input: np.array) -> np.array:
        if self._model:
            return self._model.predict(input)
        raise RuntimeError('Model not loaded yet')