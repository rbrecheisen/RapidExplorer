from widgets.viewers.dicomviewer.layer import Layer


class NumPyLayer(Layer):
    def __init__(self) -> None:
        super(NumPyLayer, self).__init__(name='numpy')