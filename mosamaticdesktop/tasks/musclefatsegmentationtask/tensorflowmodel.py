import numpy as np

from mosamaticdesktop.tasks.musclefatsegmentationtask.model import Model


class TensorFlowModel(Model):
    def __init__(self) -> None:
        super(TensorFlowModel, self).__init__()
        self._model = None

    def load(self, modelFilePath: str) -> None:
        import tensorflow as tf
        self._model = tf.keras.models.load_model(modelFilePath, compile=False)

    def predict(self, input: np.array) -> np.array:
        if self._model:
            return self._model.predict(input)
        raise RuntimeError('Model not loaded yet')